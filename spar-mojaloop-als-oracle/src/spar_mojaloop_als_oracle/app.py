# ruff: noqa: E402

from .config import Settings

_config = Settings.get_config()

from openg2p_fastapi_common.app import Initializer

from .controllers.als_oracle import ALSOracleController


class Initializer(Initializer):
    def initialize(self, **kwargs):
        # Initialize all Services, Controllers, any utils here.
        ALSOracleController().post_init()
