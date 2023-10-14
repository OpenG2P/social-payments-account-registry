from typing import List

from openg2p_fastapi_common.service import BaseService

from ..models.key_value import KeyValuePair
from ..models.selfservice import GetTxnStatus, UpdateTxnStatus
from .construct_service import ConstructService


class IdMapperService(BaseService):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.construct_service = ConstructService.get_component()

    async def get_fa_request(self, id: str) -> GetTxnStatus:
        raise NotImplementedError()

    async def get_fa_request_status(self, txn_id: str) -> UpdateTxnStatus:
        raise NotImplementedError()

    async def update_fa_request(self, id: str, fa: str) -> GetTxnStatus:
        raise NotImplementedError()

    async def update_fa_request_status(self, txn_id: str) -> UpdateTxnStatus:
        raise NotImplementedError()

    async def construct_and_get_fa_request(
        self, id_values: List[KeyValuePair], id_provider_id: int
    ) -> GetTxnStatus:
        id_constructed = await self.construct_service.id_construct(
            id_values, id_provider_id
        )
        return await self.get_fa_request(id_constructed)

    async def construct_and_update_fa_request(
        self,
        id_values: List[KeyValuePair],
        fa_values: List[KeyValuePair],
        id_provider_id: int,
        dfsp_provider_id: int,
    ) -> UpdateTxnStatus:
        id_constructed = await self.construct_service.id_construct(
            id_values, id_provider_id
        )
        fa_constructed = await self.construct_service.fa_construct(
            fa_values, dfsp_provider_id
        )
        return await self.update_fa_request(id_constructed, fa_constructed)
