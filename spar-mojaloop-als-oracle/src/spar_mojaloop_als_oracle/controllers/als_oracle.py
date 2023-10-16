import asyncio
import uuid

from starlette.status import HTTP_202_ACCEPTED

from openg2p_fastapi_common.controller import BaseController
from openg2p_common_g2pconnect_id_mapper.service.resolve import MapperResolveService

from ..config import Settings

_config = Settings.get_config()


class ALSOracleController(BaseController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mapper_resolve_service = MapperResolveService.get_component()

        self.router.tags += ["mojaloop-als-oracle"]

        self.router.add_api_route(
            "/participants/{type}/{id}",
            self.get_participants,
            status_code=HTTP_202_ACCEPTED,
            methods=["GET"],
        )

    async def get_participants(self, type: str, id: str):
        # Perform any extra validations here
        async def process_get_participants():
            pass
        asyncio.create_task(process_get_participants())
