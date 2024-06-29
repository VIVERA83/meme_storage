from core.app import Application
from image.views import image_route


def setup_routes(app: Application):
    """Конфигурирует маршруты для приложения."""
    app.include_router(image_route)
