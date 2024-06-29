from typing import Optional


from base.base_accessor import BaseAccessor
from core.settings import MinioSettings
from miniopy_async import Minio


class MinioAccessor(BaseAccessor):
    settings: Optional[MinioSettings] = None
    client: Optional[Minio] = None

    async def connect(self):
        self.settings = MinioSettings()
        self.client = Minio(
            endpoint=self.settings.minio_endpoint,
            access_key=self.settings.minio_access_key,
            secret_key=self.settings.minio_secret_key,
        )
        for bucket in self.settings.minio_buckets:
            if not await self.client.bucket_exists(bucket):
                await self.client.make_bucket(bucket)
        self.logger.info(f"{self.__class__.__name__} connected.")
