"""A module describing services for working with data."""

from store.S3.accessor import S3Accessor
from store.database.minio import MinioAccessor


class Store:
    """Data management service"""

    def __init__(self, app):
        """Initializing data sources.

        Args:
            app: The application
        """
        self.minio = MinioAccessor(app)
        self.s3 = S3Accessor(app)


def setup_store(app):
    """Configuring the connection and disconnection of storage.

    Here we inform the application about the databases of the database and other
    data sources which we run when the application is launched,
    and how to disable them.

    Args:
        app: The application
    """
    app.store = Store(app)
