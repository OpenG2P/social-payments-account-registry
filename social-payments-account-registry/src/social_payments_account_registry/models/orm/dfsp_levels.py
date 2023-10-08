from datetime import datetime
from typing import List, Optional

from openg2p_fastapi_common.context import dbengine
from openg2p_fastapi_common.models import BaseORMModel
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, select
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload

from .provider import DfspProvider


class DfspLevel(BaseORMModel):
    __tablename__ = "dfsp_levels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())
    code: Mapped[str] = mapped_column(String(20))
    level: Mapped[int] = mapped_column(Integer())

    active: Mapped[bool] = mapped_column(Boolean())

    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(), default=datetime.utcnow
    )

    @classmethod
    async def get_all_by_level(cls, level: int):
        response = []
        async_session_maker = async_sessionmaker(dbengine.get())
        async with async_session_maker() as session:
            stmt = select(cls).where(cls.level == level).order_by(cls.id.asc())

            result = await session.execute(stmt)

            response = list(result.scalars())
        return response

    @classmethod
    async def get_by_id(cls, id: int):
        result = None
        async_session_maker = async_sessionmaker(dbengine.get())
        async with async_session_maker() as session:
            result = await session.get(cls, id)

        return result


class DfspLevelValue(BaseORMModel):
    __tablename__ = "dfsp_level_values"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())
    code: Mapped[str] = mapped_column(String(20))

    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("dfsp_level_values.id"))
    parent: Mapped[Optional["DfspLevelValue"]] = relationship(
        back_populates="childs", remote_side=id
    )
    childs: Mapped[Optional[List["DfspLevelValue"]]] = relationship(
        back_populates="parent"
    )

    level_id: Mapped[int] = mapped_column(
        ForeignKey(
            "dfsp_levels.id",
        )
    )
    level: Mapped[DfspLevel] = relationship(foreign_keys=[level_id])

    next_level_id: Mapped[int] = mapped_column(ForeignKey("dfsp_levels.id"))
    next_level: Mapped[DfspLevel] = relationship(foreign_keys=[next_level_id])

    dfsp_provider_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("dfsp_providers.id")
    )
    dfsp_provider: Mapped[Optional["DfspProvider"]] = relationship()

    active: Mapped[bool] = mapped_column(Boolean())

    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(), default=datetime.utcnow
    )

    @classmethod
    async def get_all_by_level_id(cls, level_id: int):
        response = []
        async_session_maker = async_sessionmaker(dbengine.get())
        async with async_session_maker() as session:
            stmt = (
                select(cls)
                .options(selectinload(cls.level))
                .options(selectinload(cls.next_level))
                .options(selectinload(cls.dfsp_provider))
                .where(cls.level_id == level_id)
                .order_by(cls.id.asc())
            )

            result = await session.execute(stmt)

            response = list(result.scalars())
        return response
