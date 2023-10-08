from datetime import datetime
from typing import Optional

from openg2p_fastapi_common.models import BaseORMModel
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .fa_construct_strategy import FaConstructStrategy


class DfspProvider(BaseORMModel):
    __tablename__ = "dfsp_providers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())
    description: Mapped[Optional[str]] = mapped_column(String())
    code: Mapped[str] = mapped_column(String(20))
    strategy_id: Mapped[int] = mapped_column(ForeignKey("fa_construct_strategy.id"))
    strategy: Mapped["FaConstructStrategy"] = relationship()
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow)


class IdProvider(BaseORMModel):
    __tablename__ = "id_providers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())
    description: Mapped[Optional[str]] = mapped_column(String())
    code: Mapped[str] = mapped_column(String(20))
    strategy_id: Mapped[int] = mapped_column(ForeignKey("fa_construct_strategy.id"))
    strategy: Mapped["FaConstructStrategy"] = relationship()
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(), default=datetime.utcnow
    )
