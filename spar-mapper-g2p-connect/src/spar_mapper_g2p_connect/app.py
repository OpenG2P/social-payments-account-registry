# ruff: noqa: E402

from .config import Settings

_config = Settings.get_config()

from openg2p_fastapi_common.app import Initializer

from .services.g2p_connect_id_mapper import G2PConnectIdMapperService


class Initializer(Initializer):
    def initialize(self, **kwargs):
        # Initialize all Services, Controllers, any utils here.
        G2PConnectIdMapperService()
