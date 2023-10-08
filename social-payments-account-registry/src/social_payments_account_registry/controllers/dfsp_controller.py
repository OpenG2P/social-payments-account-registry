from openg2p_fastapi_common.controller import BaseController

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

    async def get_dfsp_level(self, id: int):
        return DfspLevelResponse.model_validate(await DfspLevel.get_by_id(id))

    async def get_dfsp_level_values(self, levelId: int):
        result = await DfspLevelValue.get_all_by_level_id(levelId)
        return DfspLevelValuesHttpResponse(
            levelValues=[DfspLevelValueResponse.model_validate(res) for res in result]
        )
