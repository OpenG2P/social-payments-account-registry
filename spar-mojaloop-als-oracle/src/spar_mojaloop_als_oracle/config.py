from typing import Dict

from openg2p_fastapi_common.config import Settings
from pydantic_settings import SettingsConfigDict


class Settings(Settings):
    model_config = SettingsConfigDict(
        env_prefix="spar_ml_oracle_", env_file=".env", extra="allow"
    )

    type_fa_prefix_map: Dict = {"ACCOUNT_ID": "account:"}
