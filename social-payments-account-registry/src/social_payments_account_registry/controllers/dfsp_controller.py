from typing import Annotated

from fastapi import Depends
from openg2p_fastapi_auth.dependencies import JwtBearerAuth
from openg2p_fastapi_auth.models.credentials import AuthCredentials
from openg2p_fastapi_common.controller import BaseController
from openg2p_fastapi_common.exception import BaseAppException

from ..models.dfsp import (
    DfspLevelResponse,
    DfspLevelValueResponse,
    DfspLevelValuesHttpResponse,
)
from ..models.orm.dfsp_levels import DfspLevel, DfspLevelValue


class DfspController(BaseController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.router.prefix += "/dfsp"
        self.router.tags += ["dfsp"]

        self.router.add_api_route(
            "/getLevel/{id}",
            self.get_dfsp_level,
            responses={200: {"model": DfspLevelResponse}},
            methods=["GET"],
        )
        self.router.add_api_route(
            "/getLevelValues/{levelId}",
            self.get_dfsp_level_values,
            responses={200: {"model": DfspLevelValuesHttpResponse}},
            methods=["GET"],
        )

    async def get_dfsp_level(
        self, id: int, auth: Annotated[AuthCredentials, Depends(JwtBearerAuth())]
    ):
        res = await DfspLevel.get_by_id(id)
        if res:
            return DfspLevelResponse.model_validate(res)
        else:
            raise BaseAppException("G2P-PAY-600", "DFSP Level with given id not found")

    async def get_dfsp_level_values(
        self,
        levelId: int,
        auth: Annotated[AuthCredentials, Depends(JwtBearerAuth())],
        parentId: int = None,
    ):
        result = await DfspLevelValue.get_all_by_level_id(levelId, parent_id=parentId)
        return DfspLevelValuesHttpResponse(
            levelValues=[DfspLevelValueResponse.model_validate(res) for res in result]
        )
