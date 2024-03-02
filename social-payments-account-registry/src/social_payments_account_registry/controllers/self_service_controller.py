from typing import Annotated, List, Optional

import orjson
from fastapi import Depends
from openg2p_fastapi_auth.dependencies import JwtBearerAuth
from openg2p_fastapi_auth.models.credentials import AuthCredentials
from openg2p_fastapi_common.controller import BaseController
from openg2p_fastapi_common.errors import BaseAppException

from ..models.key_value import KeyValuePair
from ..models.orm.dfsp_levels import DfspLevelValue
from ..models.orm.fa_construct_strategy import FaConstructStrategy
from ..models.orm.provider import LoginProvider
from ..models.selfservice import FaUpdateRequest, GetTxnStatus, UpdateTxnStatus
from ..services.construct_service import ConstructService
from ..services.id_mapper_service import IdMapperService


class SelfServiceController(BaseController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._id_mapper_service = IdMapperService.get_component()
        self._construct_service = ConstructService.get_component()

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
            "/updateFaRequest",
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

    @property
    def construct_service(self):
        if not self._construct_service:
            self._construct_service = ConstructService.get_component()
        return self._construct_service

    async def get_fa_request(
        self, auth: Annotated[AuthCredentials, Depends(JwtBearerAuth())]
    ):
        """
        Make a request to get the Financial Address(FA) of the authenticated user.
        - Will receive a txn_id, which can be used to query for status.
        """
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
        link: bool = False,
    ):
        """
        Make a request to update/link new FA for the authenticated user.
        - A txn_id is returned, which can be used to query for status.
        - If the user is linking their FA for the first time, the link parameter can be set.
          To check whether their FA is already linked, users can make a getFaRequest.
        - Request Json should contain level_values array, which a key value pair list.
        - Each "key" should be a valid DfspLevel's code. Use /dfsp/getLevels to get valid levels list.
        - Each "value" should be either a valid DfspLevelValue's code value, or regular string
          depending on the DfspLevel. Use /dfsp/getLevelValues to get valid values list.

        Errors:
        - Code: G2P-SPR-452. HTTP: 400. Message: Invalid value for the given
          code. &lt;Reason&gt;. &lt;Level Code&gt;.

        Internal Errors:
        - Code: G2P-SPR-450. HTTP: 500. Message: Invalid configuration of id providers and login provider.
        - Code: G2P-SPR-451. HTTP: 500. Message: Invalid configuration of dfsp providers.
        """
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
            link=link,
        )

    async def get_fa_request_status(
        self,
        txn_id: str,
        auth: Annotated[AuthCredentials, Depends(JwtBearerAuth())],
        deconstruct: Optional[bool] = False,
        deconstructCodes: Optional[bool] = True,
    ):
        """
        Get status of a getFaRequest against the given txn_id, along with FA if success.

        Errors:
        - Code: G2P-SPR-452. HTTP: 400. Message: Invalid txn_id given for get. Or the user is not allowed
          to access the txn_id.
        - Code: G2P-SPR-453. HTTP: 400. Message: Cannot deconstruct the FA using any available strategy.
        """
        # TODO: Perform validation for user vs txn
        response = await self.id_mapper_service.get_fa_request_status(txn_id)
        if deconstruct and response and response.fa:
            strategies: List[FaConstructStrategy] = await FaConstructStrategy.get_all()
            for strategy in strategies:
                res = self.construct_service.deconstruct(
                    response.fa, strategy.deconstruct_strategy
                )
                if deconstructCodes:
                    res = await self.construct_service.render_code_with_values(res)
                if res:
                    response.fa = res
                    break
            if isinstance(response.fa, str):
                raise BaseAppException(
                    "G2P-SPR-453",
                    "Cannot deconstruct the FA using any available strategy.",
                    http_status_code=400,
                )
        return response

    async def update_fa_request_status(
        self,
        txn_id: str,
        auth: Annotated[AuthCredentials, Depends(JwtBearerAuth())],
        link: bool = False,
    ):
        """
        Get status of a updateFaRequest against the given txn_id.
        - If the updateFaRequest is a link request (i.e., the link param is set), then it will have to
          be set here also. Or G2P-SPR-452 error will be thrown.
        - If the updateFaRequest is a link request even if the user has once already linked their FA,
          the status will be rejected (rjct). Vice-versa is also rejected.

        Errors:
        - Code: G2P-SPR-452. HTTP: 400. Message: Invalid txn_id given for update/link. Or the user
          is not allowed to access the txn_id.
        """
        # TODO: Perform validation for user vs txn
        return await self.id_mapper_service.update_fa_request_status(txn_id, link=link)
