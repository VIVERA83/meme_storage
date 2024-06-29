import traceback
from logging import Logger

from base.base_helper import HTTP_EXCEPTION, LOG_LEVEL
from httpcore import URL
from starlette import status
from starlette.responses import JSONResponse


class ExceptionHandler:
    """Этот класс используется для обработки всех исключений, возникающих в приложении.
    Он предоставляет стандартный способ регистрации ошибок и возврата их пользователю

    Args:
        log_level (LOG_LEVEL, optional): Используемый уровень логирования. По умолчанию "INFO".
        is_traceback (bool, optional): Включать ли трассировку в ответ. По умолчанию "False".
    """

    def __init__(self, log_level: LOG_LEVEL = "INFO", is_traceback: bool = False):
        """Инициализирует обработчик исключений.
        С заданным уровнем ведения журнала и параметрами обратной трассировки.

        """
        self.exception = Exception("Неизвестная ошибка...")
        self.level = log_level
        self.logger = Logger(__name__)
        self.message = "Неизвестная ошибка..."
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.is_traceback = is_traceback

    def __call__(
        self,
        exception: Exception,
        url: URL,
        logger: Logger = None,
        is_traceback: bool = True,
    ) -> JSONResponse:
        """Этот метод Используется для обработки исключения.

        Args:
            exception (Exception): Исключение, которое было создано.
            url (URL): URL запроса, вызвавшего исключение.
            logger (Logger, optional): Логгер для использования. По умолчанию None.
            is_traceback (bool, optional): Включать ли трассировку в ответ. По умолчанию True.

        Returns:
            JSONResponse: Ответ с деталями об исключении.
        """
        self.exception = exception
        self.logger = logger
        self.is_traceback = is_traceback
        self.handler_exception()
        return self.error_response(url)

    def error_response(self, url: URL) -> JSONResponse:
        """Этот метод используется для создания ответа с деталями об исключении.

        Args:
            url (URL): URL запроса, вызвавшего исключение.

        Returns:
            JSONResponse: Ответ с деталями об исключении.
        """
        content_data = {
            "detail": HTTP_EXCEPTION.get(self.status_code),
            "message": self.message,
        }
        if self.is_traceback:
            msg = traceback.format_exc()
        else:
            msg = f"url={url}, exception={self.exception.__class__}, message_to_user={self.exception}"
        match self.level:
            case "CRITICAL" | 50:
                msg = (
                    f" \n_____________\n "
                    f"Внимание: Произошла ошибка, на которую приложение не отреагировало корректно.."
                    f" НАМ НУЖНО СРОЧНО ОТРЕАГИРОВАТЬ"
                    f" \nExceptionHandler:  {str(self.exception)}\n"
                    f" _____________\n" + traceback.format_exc()
                )
                self.logger.critical(msg)
            case "ERROR" | 40:
                self.logger.error(msg)
            case "WARNING" | 30:
                self.logger.warning(msg)
            case _:
                self.logger.info(msg)
        return JSONResponse(content=content_data, status_code=self.status_code)

    def handler_exception(self):
        """Этот метод используется для обработки исключения.

        Он устанавливает код статуса и сообщение об ошибке.
        """
        if self.exception.args:
            self.message = self.exception.args[0]
        self.status_code = status.HTTP_400_BAD_REQUEST
        message = self.exception.__class__.__name__
        if ex := getattr(self.exception, "исключение", False):
            message += f" реальное исключение={ex.args}"
