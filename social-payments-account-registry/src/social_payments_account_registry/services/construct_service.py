import re
from typing import List

from openg2p_fastapi_common.context import dbengine
from openg2p_fastapi_common.service import BaseService
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import async_sessionmaker

from ..models.key_value import KeyValuePair
from ..models.orm.dfsp_levels import DfspLevel, DfspLevelValue
from ..models.orm.fa_construct_strategy import FaConstructStrategy
from ..models.orm.provider import DfspProvider, IdProvider


class ConstructService(BaseService):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def construct(self, values: List[KeyValuePair], strategy: str):
        return strategy.format(
            **{key_value.key: key_value.value for key_value in values}
        )

    def deconstruct(self, value: str, strategy: str) -> List[KeyValuePair]:
        regex_res = re.match(strategy, value)
        if regex_res:
            regex_res = regex_res.groupdict()
        if regex_res:
            return [KeyValuePair(key=k, value=v) for k, v in regex_res.items()]
        return []

    async def render_code_with_values(
        self, values: List[KeyValuePair]
    ) -> List[KeyValuePair]:
        if not values:
            return values
        async_session_maker = async_sessionmaker(dbengine.get())
        dfsp_levels = []
        dfsp_level_values = []
        return_list = []
        async with async_session_maker() as session:
            db_result = await session.execute(
                select(DfspLevel)
                .where(
                    and_(
                        DfspLevel.code.in_([value.key for value in values]),
                        DfspLevel.level >= 0,
                    )
                )
                .order_by(DfspLevel.level.asc())
            )
            dfsp_levels = list(db_result.scalars() or [])
            db_result = await session.execute(
                select(DfspLevel)
                .where(
                    and_(
                        DfspLevel.code.in_([value.key for value in values]),
                        DfspLevel.level < 0,
                    )
                )
                .order_by(DfspLevel.level.desc())
            )
            dfsp_levels.extend(db_result.scalars() or [])
            db_result = await session.execute(
                select(DfspLevelValue).where(
                    DfspLevelValue.code.in_([value.value for value in values])
                )
            )
            dfsp_level_values = list(db_result.scalars() or [])
        for dfsp_level in dfsp_levels:
            key_pair = next(value for value in values if value.key == dfsp_level.code)
            key_pair.key = dfsp_level.name
            return_list.append(key_pair)
            if dfsp_level.level >= 0:
                dfsp_level_value = next(
                    level_value
                    for level_value in dfsp_level_values
                    if level_value.level_id == dfsp_level.id
                )
                if dfsp_level_value:
                    key_pair.value = dfsp_level_value.name
        return return_list

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
