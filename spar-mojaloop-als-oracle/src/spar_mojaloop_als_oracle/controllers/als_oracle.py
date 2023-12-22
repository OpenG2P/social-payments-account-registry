from openg2p_fastapi_common.controller import BaseController

from ..models.participant import ParticipantsTypeIDGetResponse
from ..services.als_oracle_service import MojaloopOracleService


class ALSOracleController(BaseController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.als_oracle = MojaloopOracleService.get_component()

        self.router.tags += ["mojaloop-als-oracle"]
        self.router.prefix += "/internal/mojaloop"

        self.router.add_api_route(
            "/participants/{type}/{id}",
            self.get_participants,
            responses={200: {"model": ParticipantsTypeIDGetResponse}},
            methods=["GET"],
        )

    async def get_participants(self, type: str, id: str):
        """
        Mojaloop Get Participants API - Synchronous.
        - This is also Mojaloop ALS Oracle API. Making SPAR into Mojaloop Oracle.
        - This API can be used to return DFSP ID if the FA value is given. Example
          - If FA is "account_no:12345@abc.bank1", then this will return "bank1"
            if bank1 is the selected DFSP.

        Errors:
        - Code: ML-SPR-100. HTTP: 400. Message: Given type is not supported by this oracle.
        - Code: ML-SPR-200. HTTP: 400. Message: Given Type and ID combination is invalid or not found in this oracle.
        - Code: ML-SPR-300. HTTP: 400. Message: FinancialAddress response is not recognisable by this oracle or by Mojaloop.
        """
        return await self.als_oracle.get_participants(type, id)
