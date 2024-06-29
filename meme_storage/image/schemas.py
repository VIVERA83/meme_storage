from typing import Any, Callable, Type

import filetype
from core.settings import FileSettings
from fastapi import File
from pydantic import BaseModel, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema
from pydantic_core.core_schema import with_info_plain_validator_function
from starlette.datastructures import UploadFile


class UploadFileSchema(UploadFile):
    """Pydantic модель для проверки и разбора загружаемого входящего файла.

    Эта модель наследует от starlette.datastructures.UploadFile и добавляет
    дополнительную логику проверки и синтаксического анализа.

    Raises:
        ValueError: Если входящий файл не является экземпляром
            starlette.datastructures.UploadFile,
            или тип файла не поддерживается.
    """

    @classmethod
    def validate(cls, file: File, *_) -> Any:
        """
        Проверка входящего файла.

        Эта функция выполняет следующие проверки:

            1. входящий файл является экземпляром
               starlette.datastructures.UploadFile.
            2. Размер файла не превышает максимальное значение.
            3. Тип файла поддерживается.

        Args:
            file (File): Входящий файл.

        Returns:
            Any: Проверенный входящий файл.

        Raises:
            ValueError: Если входящий файл не является экземпляром
                starlette.datastructures.UploadFile,
                или тип файла не поддерживается.

        """
        if not isinstance(file, UploadFile):
            raise ValueError(
                f"Использован неподдерживаемый тип UploadFile, получен: {type(file)}"
            )

        file_size = FileSettings().size
        if file.size > file_size:
            max_size = file_size // 1024 // 1024
            raise ValueError(f"Размер файла не должен превышать {max_size} MB")

        if type_file := filetype.guess(file.file):
            if type_file.extension in ["jpg"]:
                return file
            raise ValueError(
                f"Неподдерживаемый тип файла: {type_file.extension}. Поддерживаемые типы: jpg."
            )
        raise ValueError("Неподдерживаемый тип файла. Поддерживаемые типы: jpg.")

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _: CoreSchema, __: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        """Этот метод переопределяет поведение Pedantic по умолчанию.

        Переопределяет поведение Pedantic по умолчанию, предоставляя
        пользовательскую схему JSON для этой модели. Схема определяет тип
        файла как строку в двоичном формате.

        Returns:
            JsonSchemaValue: Схема JSON для этой модели.

        """
        return {"type": "string", "format": "binary"}

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _: Type[Any], __r: Callable[[Any], CoreSchema]
    ) -> CoreSchema:
        """
        Определите базовую схему для этой модели.

        Этот метод переопределяет поведение Pedantic по умолчанию, предоставляя
        пользовательскую базовую схему для этой модели. Схема включает пользовательский
        метод проверки, определенный в методе validate.

        Returns:
            CoreSchema: Базовая схема для этой модели.

        """
        return with_info_plain_validator_function(cls.validate)


class OkSchema(BaseModel):
    """
    Pydantic модель для возврата ответа о статусе "успешно".

    Attributes:
        status (str): Статус "успешно".
        message (str): Сообщение о статусе.
    """

    status: str = "Оk"
    message: str = "Запрос успешно обработан."
