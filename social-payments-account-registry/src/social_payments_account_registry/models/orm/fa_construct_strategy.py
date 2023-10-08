from datetime import datetime
from typing import Optional

from openg2p_fastapi_common.models import BaseORMModel
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column


class FaConstructStrategy(BaseORMModel):
    __tablename__ = "fa_construct_strategy"

    id: Mapped[int] = mapped_column(primary_key=True)
    strategy: Mapped[str] = mapped_column(String())
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(), default=datetime.utcnow
    )
