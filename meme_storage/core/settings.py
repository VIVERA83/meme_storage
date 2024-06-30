"""Все настройки приложения."""

import os

from base.base_helper import LOG_LEVEL
from pydantic import field_validator
from pydantic_settings import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))


class Base(BaseSettings):
    class Config:
        """Настройки для чтения переменных среды из файла."""

        env_nested_delimiter = "__"
        env_file = os.path.join(BASE_DIR, ".env")
        enf_file_encoding = "utf-8"
        extra = "ignore"


class UvicornSettings(Base):
    """Uvicorn настройки.

    Args:
        host (str): Hostname.
        port (int): Port number.
        workers (int): Number of worker processes.
        log_level (str): Log level.
        reload (bool): Reload on code changes.
    """

    host: str
    port: int
    workers: int
    log_level: LOG_LEVEL = "INFO"
    reload: bool = True

    @field_validator("log_level")
    def to_lower_case(cls, log_level: LOG_LEVEL) -> str:  # noqa:
        """Convert the log level to lower case.

        Args:
            log_level (str): The log level.

        Returns:
            str: The converted log level.
        """
        return log_level.lower()


class AppSettings(Base):
    """Application settings class.

    Args:
        title (str): The name of the application.
        description (str): The description of the application.
        version (str): The version of the application.
        docs_url (str): The URL for the application's documentation.
        redoc_url (str): The URL for the application's redoc.
        openapi_url (str): The URL for the application's openapi.json.
    """

    title: str = "Image Store"
    description: str = (
        "In this service, you can generate a 'quick meme',"
        " create an image based on ready-made templates, "
        "or upload your own."
    )
    version: str = "0.0.1"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    openapi_url: str = "/openapi.json"

    app_host: str = "0.0.0.0"
    app_port: int = 8005

    @property
    def base_url(self) -> str:
        """The base URL for the application.

        Returns:
            str: The base URL for the application.
        """
        return f"http://{self.app_host}:{self.app_port}"  # noqa:


class LogSettings(Base):
    """Setting logging.

    level (str, optional): The level of logging. Defaults to "INFO".
    guru (bool, optional): Whether to enable guru mode. Defaults to True.
    traceback (bool, optional): Whether to include tracebacks in logs. Defaults to True.
    """

    level: LOG_LEVEL
    guru: bool
    traceback: bool


class FileSettings(Base):
    size: int = 1024 * 1024 * 1


class MinioSettings(Base):
    """Settings for Minio database connections."""

    minio_endpoint: str = "play.min.io"
    minio_access_key: str = "Q3AM3UQ867SPQQA43P2F"
    minio_secret_key: str = "zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG"
    minio_port: int = 9000
    minio_buckets: list[str] = ["helloworld"]
