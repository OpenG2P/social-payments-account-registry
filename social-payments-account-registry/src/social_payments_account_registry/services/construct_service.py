from typing import Dict, List

import parse
from openg2p_fastapi_common.service import BaseService

from ..models.key_value import KeyValuePair
from ..models.orm.fa_construct_strategy import FaConstructStrategy
from ..models.orm.provider import DfspProvider, IdProvider


class ConstructService(BaseService):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def construct(self, values: List[KeyValuePair], strategy: str):
        return strategy.format(
            **{key_value.key: key_value.value for key_value in values}
        )

    def deconstruct(self, value: str, strategy: str) -> Dict:
        parse_res = parse.parse(strategy, value)
        if parse_res:
            return parse_res.named
        return None

    async def id_construct(self, id_values: List[KeyValuePair], id_provider_id: int):
        id_provider: IdProvider = await IdProvider.get_by_id(id_provider_id)
        strategy: FaConstructStrategy = await FaConstructStrategy.get_by_id(
            id_provider.strategy_id
        )
        return self.construct(id_values, strategy.strategy)
        pass

    async def fa_construct(
        self, dfsp_level_values: List[KeyValuePair], dfsp_provider_id: int
    ):
        dfsp_provider: DfspProvider = await DfspProvider.get_by_id(dfsp_provider_id)
        strategy: FaConstructStrategy = await FaConstructStrategy.get_by_id(
            dfsp_provider.strategy_id
        )
        return self.construct(dfsp_level_values, strategy.strategy)
