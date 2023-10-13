# ruff: noqa: E402

import asyncio

from .config import Settings

_config = Settings.get_config()

from openg2p_fastapi_common.app import Initializer

from .controllers.dfsp_controller import DfspController
from .controllers.self_service_controller import SelfServiceController
from .models.orm.dfsp_levels import DfspLevel
from .models.orm.fa_construct_strategy import FaConstructStrategy
from .models.orm.provider import DfspProvider, IdProvider, LoginProvider


class Initializer(Initializer):
    def initialize(self, **kwargs):
        super().initialize()
        # Initialize all Services, Controllers, any utils here.
        DfspController().post_init()
        SelfServiceController().post_init()

    def migrate_database(self, args):
        super().migrate_database(args)

        async def migrate():
            await DfspProvider.create_migrate()
            await IdProvider.create_migrate()
            await FaConstructStrategy.create_migrate()
            await DfspLevel.create_migrate()
            await LoginProvider.create_migrate()

        asyncio.run(migrate())
