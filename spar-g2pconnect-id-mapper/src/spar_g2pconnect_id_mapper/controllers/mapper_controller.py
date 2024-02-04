import asyncio
import uuid
from datetime import datetime

from openg2p_common_g2pconnect_id_mapper.models.common import (
    Ack,
    CommonResponse,
    CommonResponseMessage,
)
from openg2p_common_g2pconnect_id_mapper.models.link import LinkHttpRequest
from openg2p_common_g2pconnect_id_mapper.models.resolve import ResolveHttpRequest
from openg2p_common_g2pconnect_id_mapper.models.update import UpdateHttpRequest
from openg2p_fastapi_common.controller import BaseController
from openg2p_fastapi_common.errors import BaseAppException

from ..services.mapper_service import MapperService


class MapperController(BaseController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.mapper_service = MapperService.get_component()

        self.router.prefix += "/mapper"
        self.router.tags += ["mapper-async"]

        self.router.add_api_route(
            "/link",
            self.link,
            responses={200: {"model": CommonResponseMessage}},
            methods=["POST"],
        )
        self.router.add_api_route(
            "/update",
            self.update,
            responses={200: {"model": CommonResponseMessage}},
            methods=["POST"],
        )
        self.router.add_api_route(
            "/resolve",
            self.resolve,
            responses={200: {"model": CommonResponseMessage}},
            methods=["POST"],
        )
        self.router.add_api_route(
            "/unlink",
            self.unlink,
            responses={200: {"model": CommonResponseMessage}},
            methods=["POST"],
        )

    async def link(self, request: LinkHttpRequest):
        if request.header.action != "link":
            raise BaseAppException(
                code="MPR-REQ-400",
                message="Received Invalid action in header for 'link'.",
                http_status_code=400,
            )

        # TODO: For now returning random correlation id.
        correlation_id = str(uuid.uuid4())
        # TODO: For now creating async task and forgetting
        asyncio.create_task(self.mapper_service.link(correlation_id, request))

        return CommonResponseMessage(
            message=CommonResponse(
                ack_status=Ack.ACK,
                correlation_id=correlation_id,
                timestamp=datetime.utcnow(),
            )
        )

    async def update(self, request: UpdateHttpRequest):
        if request.header.action != "update":
            raise BaseAppException(
                code="MPR-REQ-400",
                message="Received Invalid action in header for 'update'.",
                http_status_code=400,
            )
        # TODO: For now returning random correlation id.
        correlation_id = str(uuid.uuid4())
        # TODO: For now creating async task and forgetting
        asyncio.create_task(self.mapper_service.update(correlation_id, request))

        return CommonResponseMessage(
            message=CommonResponse(
                ack_status=Ack.ACK,
                correlation_id=correlation_id,
                timestamp=datetime.utcnow(),
            )
        )

    async def resolve(self, request: ResolveHttpRequest):
        if request.header.action != "resolve":
            raise BaseAppException(
                code="MPR-REQ-400",
                message="Received Invalid action in header for 'resolve'.",
                http_status_code=400,
            )
        # TODO: For now returning random correlation id.
        correlation_id = str(uuid.uuid4())
        # TODO: For now creating async task and forgetting
        asyncio.create_task(self.mapper_service.resolve(correlation_id, request))

        return CommonResponseMessage(
            message=CommonResponse(
                ack_status=Ack.ACK,
                correlation_id=correlation_id,
                timestamp=datetime.utcnow(),
            )
        )

    async def unlink(self):
        raise NotImplementedError()
