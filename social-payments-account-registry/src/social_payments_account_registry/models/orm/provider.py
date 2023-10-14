from typing import Optional

from openg2p_fastapi_auth.models.orm.login_provider import (
    LoginProvider as OriginalLoginProvider,
)
from openg2p_fastapi_common.models import BaseORMModelWithTimes
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .fa_construct_strategy import FaConstructStrategy


class DfspProvider(BaseORMModelWithTimes):
    __tablename__ = "dfsp_providers"

    name: Mapped[str] = mapped_column(String())
    description: Mapped[Optional[str]] = mapped_column(String())
    code: Mapped[str] = mapped_column(String(20))
    strategy_id: Mapped[int] = mapped_column(ForeignKey("fa_construct_strategy.id"))
    strategy: Mapped["FaConstructStrategy"] = relationship()


class IdProvider(BaseORMModelWithTimes):
    __tablename__ = "id_providers"

    name: Mapped[str] = mapped_column(String())
    description: Mapped[Optional[str]] = mapped_column(String())
    code: Mapped[str] = mapped_column(String(20))
    strategy_id: Mapped[int] = mapped_column(ForeignKey("fa_construct_strategy.id"))
    strategy: Mapped["FaConstructStrategy"] = relationship()


class LoginProvider(OriginalLoginProvider):
    id_provider_id: Mapped[Optional[int]] = mapped_column(ForeignKey("id_providers.id"))
    id_provider: Mapped[Optional[IdProvider]] = relationship()
