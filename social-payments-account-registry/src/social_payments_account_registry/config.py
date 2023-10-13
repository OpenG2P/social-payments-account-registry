from openg2p_fastapi_auth.config import ApiAuthSettings
from openg2p_fastapi_auth.config import Settings as AuthSettings
from openg2p_fastapi_common.config import Settings
from pydantic_settings import SettingsConfigDict


class Settings(AuthSettings, Settings):
    model_config = SettingsConfigDict(
        env_prefix="spar_core_", env_file=".env", extra="allow"
    )

    openapi_title: str = "Social Payments Account Registry"
    openapi_description: str = """
    This module gives selfservice portal and additional functionalities to an ID Account Mapper, like G2P Connect.

    ***********************************
    Further details goes here
    ***********************************
    """
    openapi_version: str = "0.1.0"

    auth_enabled: bool = True
    auth_api_get_dfsp_level: ApiAuthSettings = ApiAuthSettings(enabled=True)
