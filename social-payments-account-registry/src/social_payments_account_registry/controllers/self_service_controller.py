from openg2p_fastapi_common.controller import BaseController


class SelfServiceController(BaseController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.router.prefix += "/selfservice"
        self.router.tags += ["selfservice"]

        self.router.add_api_route(
            "/getFaRequest",
            self.get_fa_request,
            # responses={200: {"model": }},
            methods=["POST"],
        )
        self.router.add_api_route(
            "/getFaRequestStatus",
            self.get_fa_request_status,
            # responses={200: {"model": }},
            methods=["GET"],
        )
        self.router.add_api_route(
            "/updateFaRequest",
            self.update_fa_request,
            # responses={200: {"model": }},
            methods=["POST"],
        )
        self.router.add_api_route(
            "/updateFaRequestStatus",
            self.update_fa_request_status,
            # responses={200: {"model": }},
            methods=["GET"],
        )

    async def get_fa_request(self):
        pass

    async def get_fa_request_status(self):
        pass

    async def update_fa_request(self):
        pass

    async def update_fa_request_status(self):
        pass
