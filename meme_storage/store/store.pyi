from core.app import ApplicationImage
from store.S3.helper import S3Accessor
from store.database.minio import MinioAccessor

class Store:
    """Data management service"""

    minio: MinioAccessor
    s3: S3Accessor

    def __init__(self, app: ApplicationImage):
        """
        Initialize the store.

        Args:
            app (Application): The main application component.
        """

def setup_store(app: ApplicationImage):
    app.store = Store(app)
