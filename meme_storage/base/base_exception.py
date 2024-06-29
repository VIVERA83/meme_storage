class ExceptionBase(Exception):
    """Базовый класс исключений"""

    args = "Неизвестная ошибка"
    exception = None

    def __init__(self, *args, exception: Exception = None):
        if args:
            self.args = args
        if exception:
            self.exception = exception

    def __str__(self):
        return f"Ошибка: {self.args[0]}"
