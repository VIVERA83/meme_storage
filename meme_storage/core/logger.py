import logging
import sys

from core.settings import LogSettings
from loguru import logger


def setup_logging() -> logging.Logger:
    """Настройка логирования.

    В этом случае есть возможность использовать "logoru".
    https://github.com/Delgan/loguru
    """
    settings = LogSettings()
    if settings.guru:
        logger.configure(
            **{
                "handlers": [
                    {
                        "sink": sys.stderr,
                        "level": settings.level,
                        "backtrace": settings.traceback,
                    },
                ],
            }
        )
        logger.info("Ведение журнала с использованием 'logoru'")
        return logger
    logging.basicConfig(level=settings.log_level)
    loger = logging.getLogger(__name__)
    logging.info("Ведение журнала с использованием logging.basicConfig")
    return loger
