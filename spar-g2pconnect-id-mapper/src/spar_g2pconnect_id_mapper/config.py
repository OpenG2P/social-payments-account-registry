from typing import Optional

from openg2p_fastapi_common.config import Settings
from pydantic import AnyUrl
from pydantic_settings import SettingsConfigDict

from . import __version__


class Settings(Settings):
    model_config = SettingsConfigDict(
        env_prefix="spar_g2pconnect_mapper_", env_file=".env", extra="allow"
    )

    openapi_title: str = "SPAR G2P Connect ID Account Mapper"
    openapi_description: str = """
    This module implements G2P ID Account Mapper (Financial Address Mapper).

    ***********************************
    Further details goes here
    ***********************************
    """
    openapi_version: str = __version__

    db_dbname: str = "spardb"

    default_callback_url: Optional[AnyUrl] = None
    callback_sender_id: str = "spar.dev.openg2p.net"
