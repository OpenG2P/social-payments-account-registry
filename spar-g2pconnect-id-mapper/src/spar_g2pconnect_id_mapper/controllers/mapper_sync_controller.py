import uuid

from openg2p_common_g2pconnect_id_mapper.models.link import (
    LinkCallbackHttpRequest,
    LinkHttpRequest,
)
from openg2p_common_g2pconnect_id_mapper.models.resolve import (
    ResolveCallbackHttpRequest,
    ResolveHttpRequest,
)
from openg2p_common_g2pconnect_id_mapper.models.update import (
    UpdateCallbackHttpRequest,
    UpdateHttpRequest,
)
from openg2p_fastapi_common.controller import BaseController
from openg2p_fastapi_common.errors import BaseAppException

from ..services.mapper_service import MapperService


class MapperSyncController(BaseController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.mapper_service = MapperService.get_component()

        self.router.prefix += "/mapper/sync"
        self.router.tags += ["mapper-sync"]

        self.router.add_api_route(
            "/link",
            self.link_sync,
            responses={200: {"model": LinkCallbackHttpRequest}},
            methods=["POST"],
        )
        self.router.add_api_route(
            "/update",
            self.update_sync,
            responses={200: {"model": UpdateCallbackHttpRequest}},
            methods=["POST"],
        )
        self.router.add_api_route(
            "/resolve",
            self.resolve_sync,
            responses={200: {"model": ResolveCallbackHttpRequest}},
            methods=["POST"],
        )
        self.router.add_api_route(
            "/unlink",
            self.unlink_sync,
            # TODO
            responses={200: {"model": ResolveCallbackHttpRequest}},
            methods=["POST"],
        )

    async def link_sync(self, request: LinkHttpRequest):
        if request.header.action != "link":
            raise BaseAppException(
                code="MPR-REQ-400",
                message="Received Invalid action in header for 'link'.",
                http_status_code=400,
            )

        # TODO: For now returning random correlation id.
        correlation_id = str(uuid.uuid4())
        # TODO: For now creating async task and forgetting

        return await self.mapper_service.link(
            correlation_id, request, make_callback=False
        )

    async def update_sync(self, request: UpdateHttpRequest):
        if request.header.action != "update":
            raise BaseAppException(
                code="MPR-REQ-400",
                message="Received Invalid action in header for 'update'.",
                http_status_code=400,
            )
        # TODO: For now returning random correlation id.
        correlation_id = str(uuid.uuid4())
        # TODO: For now creating async task and forgetting
        return await self.mapper_service.update(
            correlation_id, request, make_callback=False
        )

    async def resolve_sync(self, request: ResolveHttpRequest):
        if request.header.action != "resolve":
            raise BaseAppException(
                code="MPR-REQ-400",
                message="Received Invalid action in header for 'resolve'.",
                http_status_code=400,
            )
        # TODO: For now returning random correlation id.
        correlation_id = str(uuid.uuid4())
        # TODO: For now creating async task and forgetting
        return await self.mapper_service.resolve(
            correlation_id, request, make_callback=False
        )

    async def unlink_sync(self):
        raise NotImplementedError()
