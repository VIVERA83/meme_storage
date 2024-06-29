"""Модуль для настройки приложения."""

from core.app import Application
from core.logger import setup_logging
from core.middelware import setup_middleware
from core.routes import setup_routes
from core.settings import AppSettings
from store.store import setup_store


def setup_app(*_, **__) -> "Application":
    """Создание и настройка основного FastAPI приложения.

    Returns:
        Application: Основное FastAPI приложение.
    """
    settings = AppSettings()
    app = Application(
        docs_url=settings.docs_url,
        redoc_url=settings.redoc_url,
        openapi_url=settings.openapi_url,
        version=settings.version,
        title=settings.title,
        description=settings.description,
    )
    app.settings = settings
    app.logger = setup_logging()
    setup_store(app)
    setup_middleware(app)
    setup_routes(app)
    app.logger.info(f"Swagger link: {app.settings.base_url}{app.docs_url}")
    return app
