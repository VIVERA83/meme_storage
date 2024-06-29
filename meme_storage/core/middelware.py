import re

from core.app import Application
from core.exception_handler import ExceptionHandler
from core.settings import LogSettings
from fastapi import Request as FastApiRequest
from fastapi import Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Пользовательское промежуточное программное обеспечение
     для обработки исключений и ошибок в приложении Fast API.

    Args:
        app (ASGIApp): Экземпляр приложения Fast API.

    Attributes:
        settings (LogSettings): Настройки логирования.
        exception_handler (ExceptionHandler): Обработчик исключений.
    """

    def __init__(self, app: ASGIApp, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.settings = LogSettings()
        self.exception_handler = ExceptionHandler(
            self.settings.level,
            self.settings.traceback,
        )

    async def dispatch(
        self, request: FastApiRequest, call_next: RequestResponseEndpoint
    ) -> Response:
        """.

        Args:
            request (FastApiRequest): The incoming request.
            call_next (RequestResponseEndpoint): The next middleware or the
                application.

        Raises:
            Exception: Any exception raised by the next middleware or the
                application.

        Returns:
            Response: The response from the next middleware or the application.
        """
        try:
            self.is_endpoint(request)
            response = await call_next(request)
            return response
        except Exception as error:
            return self.exception_handler(
                error,
                request.url,
                request.app.logger,
                self.settings.traceback,
            )

    @staticmethod
    def is_endpoint(request: FastApiRequest) -> bool:
        """Проверьте, является ли запрос конечной точкой.

        Args:
            request (FastApiRequest): Входящий запрос.

        Raises:
            HTTPException: Если запрос не является конечной точкой.

        Returns:
            bool: True, если запрос является конечной точкой.
        """
        detail = "{message}, См. документацию: http://{host}:{port}{uri}"  # noqa
        message = "Не найдено"
        status_code = status.HTTP_404_NOT_FOUND
        for route in request.app.routes:
            if re.match(route.path_regex, request.url.path):
                if request.method.upper() in route.methods:
                    return True
                status_code = status.HTTP_405_METHOD_NOT_ALLOWED
                message = "Метод не поддерживается"
        raise HTTPException(
            status_code,
            detail.format(
                message=message,
                host=request.app.settings.app_host,
                port=request.app.settings.app_port,
                uri=request.app.docs_url,
            ),
        )


async def validation_exception_handler(
    _: FastApiRequest, exc: RequestValidationError
) -> JSONResponse:
    """Пользовательский обработчик исключений для валидации запроса.

    Args:
        _ (FastApiRequest): Входящий запрос.
        exc (RequestValidationError): Исключение.

    Returns:
        JSONResponse: Ответ с деталями об исключении.
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            {"detail": "Bad request", "message": exc.errors()[0].get("msg")}
        ),
    )


def setup_middleware(app: Application):
    """Настройка промежуточного программного обеспечения для FastAPI.

    Args:
        app (Application): Экземпляр приложения.

    Raises:
        Exception: Если произошло исключение.
    """
    app.exception_handler(RequestValidationError)(validation_exception_handler)
    app.add_middleware(ErrorHandlingMiddleware)
