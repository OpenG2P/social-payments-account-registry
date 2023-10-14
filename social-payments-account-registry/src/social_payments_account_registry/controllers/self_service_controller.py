from typing import Annotated

import orjson
from fastapi import Depends
from openg2p_fastapi_auth.dependencies import JwtBearerAuth
from openg2p_fastapi_auth.models.credentials import AuthCredentials
from openg2p_fastapi_common.controller import BaseController
from openg2p_fastapi_common.errors import BaseAppException

from ..models.key_value import KeyValuePair
from ..models.orm.dfsp_levels import DfspLevelValue
from ..models.orm.provider import LoginProvider
from ..models.selfservice import FaUpdateRequest, GetTxnStatus, UpdateTxnStatus
from ..services.id_mapper_service import IdMapperService


class SelfServiceController(BaseController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._id_mapper_service = IdMapperService.get_component()

        self.router.prefix += "/selfservice"
        self.router.tags += ["selfservice"]

        self.router.add_api_route(
            "/getFaRequest",
            self.get_fa_request,
            responses={200: {"model": GetTxnStatus}},
            methods=["POST"],
        )
        self.router.add_api_route(
            "/getFaRequestStatus/{txn_id}",
            self.get_fa_request_status,
            responses={200: {"model": GetTxnStatus}},
            methods=["GET"],
        )
        self.router.add_api_route(
            "/updateFaRequest/",
            self.update_fa_request,
            responses={200: {"model": UpdateTxnStatus}},
            methods=["POST"],
        )
        self.router.add_api_route(
            "/updateFaRequestStatus/{txn_id}",
            self.update_fa_request_status,
            responses={200: {"model": UpdateTxnStatus}},
            methods=["GET"],
        )

    @property
    def id_mapper_service(self):
        if not self._id_mapper_service:
            self._id_mapper_service = IdMapperService.get_component()
        return self._id_mapper_service

    async def get_fa_request(
        self, auth: Annotated[AuthCredentials, Depends(JwtBearerAuth())]
    ):
        login_provider: LoginProvider = await LoginProvider.get_login_provider_from_iss(
            auth.iss
        )
        return await self.id_mapper_service.construct_and_get_fa_request(
            [
                KeyValuePair(
                    key=key,
                    value=value
                    if isinstance(value, str)
                    else orjson.dumps(value).decode(),
                )
                for key, value in auth.model_dump().items()
            ],
            login_provider.id_provider_id,
        )

    async def update_fa_request(
        self,
        fa_update_request: FaUpdateRequest,
        auth: Annotated[AuthCredentials, Depends(JwtBearerAuth())],
    ):
        # TODO: Perform Validations on input
        login_provider: LoginProvider = await LoginProvider.get_login_provider_from_iss(
            auth.iss
        )
        if (not login_provider) or (not login_provider.id_provider_id):
            raise BaseAppException(
                "G2P-SPR-450",
                "Invalid configuration of id providers and login provider",
            )
        dfsp_level_value = await DfspLevelValue.get_last_dfsp_provider_for_codes(
            [key_value.value for key_value in fa_update_request.level_values]
        )
        if not dfsp_level_value:
            raise BaseAppException(
                "G2P-SPR-451", "Invalid configuration of dfsp providers."
            )

        return await self.id_mapper_service.construct_and_update_fa_request(
            [
                KeyValuePair(
                    key=key,
                    value=value
                    if isinstance(value, str)
                    else orjson.dumps(value).decode(),
                )
                for key, value in auth.model_dump().items()
            ],
            fa_update_request.level_values,
            login_provider.id_provider_id,
            dfsp_level_value.dfsp_provider_id,
        )

    async def get_fa_request_status(
        self, txn_id: str, auth: Annotated[AuthCredentials, Depends(JwtBearerAuth())]
    ):
        # TODO: Perform validation for user vs txn
        return await self.id_mapper_service.get_fa_request_status(txn_id)

    async def update_fa_request_status(
        self, txn_id: str, auth: Annotated[AuthCredentials, Depends(JwtBearerAuth())]
    ):
        # TODO: Perform validation for user vs txn
        return await self.id_mapper_service.update_fa_request_status(txn_id)
