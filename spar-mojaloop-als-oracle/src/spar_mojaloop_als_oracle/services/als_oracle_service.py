from typing import List

from openg2p_common_g2pconnect_id_mapper.models.common import (
    MapperValue,
    RequestStatusEnum,
)
from openg2p_common_g2pconnect_id_mapper.service.resolve import MapperResolveService
from openg2p_fastapi_common.service import BaseService
from social_payments_account_registry.models.orm.fa_construct_strategy import (
    FaConstructStrategy,
)
from social_payments_account_registry.models.orm.provider import DfspProvider
from social_payments_account_registry.services.construct_service import ConstructService

from ..config import Settings
from ..errors import BaseMojaloopException
from ..models.participant import ParticipantsTypeIDGetResponse, PartyTypeIdInfo

_config = Settings.get_config()


class MojaloopOracleService(BaseService):
    def __init__(self, name="", **kwargs):
        super().__init__(name=name, **kwargs)

        self.mapper_resolve_service = MapperResolveService.get_component()
        self.construct_service = ConstructService.get_component()

    async def get_participants(self, type: str, id: str):
        if type not in _config.type_fa_prefix_map:
            # Make this compliant to Mojaloop
            raise BaseMojaloopException(
                "ML-SPR-100",
                "Given type is not supported by this oracle.",
                http_status_code=400,
            )

        fa_prefix = _config.type_fa_prefix_map[type]

        response = None
        # The Following is only possible if the ID Mapper allows
        # seaching through the FAs using the resolve API.
        # This is possible in Sunbird's G2P ID Mapper because of a limitation
        try:
            res = await self.mapper_resolve_service.resolve_request(
                [
                    MapperValue(
                        fa=f"{fa_prefix}{id}",
                    ),
                ],
                loop_sleep=0,
                max_retries=100,
            )
            res = list(res.refs.values())[0]
            if res.status == RequestStatusEnum.succ:
                response = res.fa
        except Exception as e:
            raise BaseMojaloopException(
                "ML-SPR-200",
                "Given Type and ID combination is invalid or not found in this oracle.",
                http_status_code=400,
            ) from e

        if not response:
            raise BaseMojaloopException(
                "ML-SPR-200",
                "Given Type and ID combination is invalid or not found in this oracle.",
                http_status_code=400,
            )

        dfsp_id: str = None

        dfsp_providers: List[DfspProvider] = await DfspProvider.get_all()
        for dfsp_prov in dfsp_providers:
            strategy: FaConstructStrategy = await FaConstructStrategy.get_by_id(
                dfsp_prov.strategy_id
            )
            res = self.construct_service.deconstruct(response, strategy.strategy)
            if res and dfsp_prov.code in [i.value for i in res]:
                dfsp_id = dfsp_prov.code
                break

        if not dfsp_id:
            raise BaseMojaloopException(
                "ML-SPR-300",
                "FinancialAddress response is not recognisable by this oracle or by Mojaloop.",
                http_status_code=400,
            )

        return ParticipantsTypeIDGetResponse(
            partyList=[
                PartyTypeIdInfo(fspId=dfsp_id),
            ]
        )
