from openg2p_fastapi_common.models import BaseORMModelWithTimes
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class FaConstructStrategy(BaseORMModelWithTimes):
    __tablename__ = "fa_construct_strategy"

    strategy: Mapped[str] = mapped_column(String())
