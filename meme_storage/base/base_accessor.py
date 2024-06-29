class BaseAccessor:
    """Базовый класс, отвечающий за привязку логики к базовому приложению."""

    def __init__(self, app):
        """Инициализируем подключение к основному приложению Fast Api.

        Args:
            app (FastAPI): Приложение Fast Api
        """
        self.app = app
        self.logger = app.logger
        app.on_event("startup")(self.connect)
        app.on_event("shutdown")(self.disconnect)
        self._init()

    def _init(self):
        """Описание дополнительных действий для инициализации."""

    async def connect(self):
        """Логика, отвечающая за подключение и настройку.

        В качестве примера настраивается подключение к стороннему API.
        """
        self.logger.info(f"{self.__class__.__name__} успешно подключено")

    async def disconnect(self):
        """Логика, отвечающая за отключение и очистку.

        Обеспечивает правильное завершение всех соединений.
        """
        self.logger.info(f"{self.__class__.__name__} успешно отключено")
