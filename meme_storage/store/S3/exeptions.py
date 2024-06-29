from base.base_exception import ExceptionBase


class S3FileNotFoundException(ExceptionBase):
    args = (
        "Запрошенный объект по указанному адресу не найден в S3 сервере. "
        "Возможно, он был удалён, переименован или указан некорректно адрес ресурса.",
    )


class S3ConnectionErrorException(ExceptionBase):
    args = ("Не удалось подключиться к S3 серверу. Повторите попытку позже.",)


class S3UnknownException(ExceptionBase):
    args = ("Неизвестная ошибка S3 сервера.",)


class S3BucketNotFoundException(ExceptionBase):
    args = ("Запрошенный бакет не найден в S3 сервере.",)
