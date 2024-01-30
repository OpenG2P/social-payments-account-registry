# ruff: noqa: E402

import asyncio

from .config import Settings

_config = Settings.get_config()

from openg2p_fastapi_common.app import Initializer

from .controllers.mapper_controller import MapperController
from .controllers.mapper_sync_controller import MapperSyncController
from .models.orm.id_fa_mapping import IdFaMapping
from .services.mapper_service import MapperService


class Initializer(Initializer):
    def initialize(self, **kwargs):
        super().initialize(**kwargs)
        MapperService()
        MapperController().post_init()
        MapperSyncController().post_init()

    def migrate_database(self, args):
        super().migrate_database(args)

        async def migrate():
            await IdFaMapping.create_migrate()

        asyncio.run(migrate())
