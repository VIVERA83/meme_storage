import logging

from core.settings import AppSettings
from fastapi import FastAPI
from fastapi import Request as FastAPIRequest
from store.store import Store


class Application(FastAPI):
    """Основной класс приложения.

    Этот класс отвечает за инициализацию приложения Fast API,
    а также за управление зависимостями и конфигурацией приложения.

    Attributes:
        store (Store): Экземпляр хранилища.
        settings (AppSettings): Настройки приложения.
        logger (logging.Logger): Экземпляр логгера.
        docs_url (str): URL-адрес документации.
    """

    store: Store
    settings: AppSettings
    logger: logging.Logger
    docs_url: str


class Request(FastAPIRequest):
    """Request переопределение.

    Чтобы IDE правильно подсказывала объявления методов.
    """

    app: Application
