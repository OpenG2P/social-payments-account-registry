from typing import Annotated, Optional

from fastapi import Depends, Query
from openg2p_fastapi_auth.dependencies import JwtBearerAuth
from openg2p_fastapi_auth.models.credentials import AuthCredentials
from openg2p_fastapi_common.controller import BaseController

from ..models.dfsp import (
    DfspLevelHttpResponse,
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
            "/getLevels",
            self.get_dfsp_level,
            responses={200: {"model": DfspLevelHttpResponse}},
            methods=["GET"],
        )
        self.router.add_api_route(
            "/getLevelValues",
            self.get_dfsp_level_values,
            responses={200: {"model": DfspLevelValuesHttpResponse}},
            methods=["GET"],
        )

    async def get_dfsp_level(
        self,
        auth: Annotated[AuthCredentials, Depends(JwtBearerAuth())],
        id: Optional[int] = Query(None, description="Filter for levels with this ID"),
        code: Optional[str] = Query(
            None, description="Filter for level with this code."
        ),
        level: Optional[int] = Query(
            None, description="Filter for levels with this level number"
        ),
    ):
        """
        Get Levels that can be supplied to Update FA Request. Or to be shown on UI.
        - Authentication required.
        - A combination of the query parameters can be used.
        """
        result = await DfspLevel.get_all_by_query(id=id, code=code, level=level)
        return DfspLevelHttpResponse(
            levels=[DfspLevelResponse.model_validate(res) for res in result]
        )

    async def get_dfsp_level_values(
        self,
        auth: Annotated[AuthCredentials, Depends(JwtBearerAuth())],
        id: Optional[int] = Query(
            None, description="Filter for level Values with this ID."
        ),
        code: Optional[str] = Query(
            None, description="Filter for level Values with this code."
        ),
        levelId: Optional[int] = Query(
            None, description="Filter for level values whose level's ID is this."
        ),
        parentId: Optional[int] = Query(
            None,
            description="Filter for level values whose parent Level value's ID is this.",
        ),
    ):
        """
        Get Level Values that can be supplied to each particular level in the Update FA Request.
        Or to be shown on UI.
        - Authentication required.
        - A combination of the query parameters can be used.
        """
        result = await DfspLevelValue.get_all_by_query(
            id=id, code=code, level_id=levelId, parent_id=parentId
        )
        return DfspLevelValuesHttpResponse(
            levelValues=[DfspLevelValueResponse.model_validate(res) for res in result]
        )
