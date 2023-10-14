from openg2p_common_g2pconnect_id_mapper.config import (
    Settings as G2PConnectMapperSettings,
)
from openg2p_fastapi_common.config import Settings
from pydantic_settings import SettingsConfigDict


class Settings(G2PConnectMapperSettings, Settings):
    model_config = SettingsConfigDict(
        env_prefix="spar_g2p_connect_", env_file=".env", extra="allow"
    )
