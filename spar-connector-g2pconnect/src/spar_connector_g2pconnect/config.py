from openg2p_common_g2pconnect_id_mapper.config import (
    Settings as G2PConnectMapperSettings,
)
from openg2p_fastapi_common.config import Settings
from pydantic_settings import SettingsConfigDict


class Settings(G2PConnectMapperSettings, Settings):
    model_config = SettingsConfigDict(
        env_prefix="spar_connector_g2pconnect_", env_file=".env", extra="allow"
    )

    callback_api_common_prefix: str = "/internal/callback"

    mapper_resolve_sender_url: str = "http://localhost:8000/internal/callback/mapper"
    mapper_link_sender_url: str = "http://localhost:8000/internal/callback/mapper"
    mapper_update_sender_url: str = "http://localhost:8000/internal/callback/mapper"
