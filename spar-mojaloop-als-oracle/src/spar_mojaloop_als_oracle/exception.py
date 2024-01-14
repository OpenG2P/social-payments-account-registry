import logging

from fastapi.responses import ORJSONResponse
from openg2p_fastapi_common.component import BaseComponent
from openg2p_fastapi_common.context import app_registry

from .config import Settings
from .errors import BaseMojaloopException
from .models.error import ErrorInformation, ErrorInformationResponse

_config = Settings.get_config()
_logger = logging.getLogger(_config.logging_default_logger_name)


class ExceptionHandler(BaseComponent):
    def __init__(self, name="", **kwargs):
        super().__init__(name=name)

        app_registry.get().add_exception_handler(
            BaseMojaloopException, self.base_mojaloop_exception_handler
        )

    async def base_mojaloop_exception_handler(
        self, request, exc: BaseMojaloopException
    ):
        _logger.exception(f"Received Mojaloop Exception: {exc}")
        res = ErrorInformationResponse(
            errorInformation=ErrorInformation(
                errorCode=exc.code,
                errorDescription=exc.message,
            ),
        )
        return ORJSONResponse(
            content=res.model_dump(), status_code=exc.status_code, headers=exc.headers
        )
