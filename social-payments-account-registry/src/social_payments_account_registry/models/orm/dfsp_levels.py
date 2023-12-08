from typing import List, Optional

from openg2p_fastapi_common.context import dbengine
from openg2p_fastapi_common.models import BaseORMModelWithTimes
from sqlalchemy import ForeignKey, Integer, String, and_, select
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload

from .provider import DfspProvider


class DfspLevel(BaseORMModelWithTimes):
    __tablename__ = "dfsp_levels"

    name: Mapped[str] = mapped_column(String())
    code: Mapped[str] = mapped_column(String(20))
    level: Mapped[int] = mapped_column(Integer())

    next_level_id: Mapped[Optional[int]] = mapped_column(ForeignKey("dfsp_levels.id"))
    next_level: Mapped[Optional["DfspLevel"]] = relationship(
        foreign_keys=[next_level_id]
    )

    validation_regex: Mapped[Optional[str]] = mapped_column(String())

    @classmethod
    async def get_all_by_query(cls, **kwargs):
        if "active" not in kwargs:
            kwargs["active"] = True
        response = []
        async_session_maker = async_sessionmaker(dbengine.get())
        async with async_session_maker() as session:
            stmt = select(cls).options(selectinload(cls.next_level))
            for key, value in kwargs.items():
                if value is not None:
                    stmt = stmt.where(getattr(cls, key) == value)

            stmt = stmt.order_by(cls.id.asc())

            result = await session.execute(stmt)

            response = list(result.scalars())
        return response


class DfspLevelValue(BaseORMModelWithTimes):
    __tablename__ = "dfsp_level_values"

    name: Mapped[str] = mapped_column(String())
    code: Mapped[str] = mapped_column(String(20))

    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("dfsp_level_values.id"))

    level_id: Mapped[int] = mapped_column(ForeignKey("dfsp_levels.id"))
    level: Mapped[DfspLevel] = relationship(foreign_keys=[level_id])

    next_level_id: Mapped[int] = mapped_column(ForeignKey("dfsp_levels.id"))
    next_level: Mapped[DfspLevel] = relationship(foreign_keys=[next_level_id])

    dfsp_provider_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("dfsp_providers.id")
    )
    dfsp_provider: Mapped[Optional["DfspProvider"]] = relationship()

    @classmethod
    async def get_all_by_query(cls, **kwargs):
        if "active" not in kwargs:
            kwargs["active"] = True
        response = []
        async_session_maker = async_sessionmaker(dbengine.get())
        async with async_session_maker() as session:
            stmt = (
                select(cls)
                .options(selectinload(cls.level))
                .options(selectinload(cls.next_level))
                .options(selectinload(cls.dfsp_provider))
            )
            for key, value in kwargs.items():
                if value is not None:
                    stmt = stmt.where(getattr(cls, key) == value)

            stmt = stmt.order_by(cls.id.asc())

            result = await session.execute(stmt)

            response = list(result.scalars())
        return response

    @classmethod
    async def get_last_dfsp_provider_for_codes(cls, codes: List[str]):
        result = None
        async_session_maker = async_sessionmaker(dbengine.get())
        async with async_session_maker() as session:
            stmt = (
                select(cls)
                .join(cls.level)
                .where(and_(cls.code.in_(codes), cls.dfsp_provider_id.isnot(None)))
                .order_by(DfspLevel.level.desc())
            )

            res = (await session.execute(stmt)).scalar()

            if res:
                result = res
        return result
