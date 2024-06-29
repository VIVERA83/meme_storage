import aiohttp

from base.base_accessor import BaseAccessor
from image.schemas import UploadFileSchema
from starlette.responses import StreamingResponse

from store.S3.exeptions import (
    S3ConnectionErrorException,
    S3UnknownException,
    S3FileNotFoundException,
    S3BucketNotFoundException,
)


def exception_handler(func):
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except IOError as e:
            if e.errno == 111:
                raise S3ConnectionErrorException(exception=e)
        except ValueError as e:
            raise S3BucketNotFoundException(exception=e)
        except KeyError as e:
            raise S3FileNotFoundException(exception=e)
        except Exception as e:
            if code := getattr(e, "code", None):
                if code == "NoSuchBucket":
                    raise S3BucketNotFoundException()
                if code == "NoSuchKey":
                    raise S3FileNotFoundException()
        raise S3UnknownException()

    return wrapper


class S3Accessor(BaseAccessor):

    @exception_handler
    async def upload(self, bucket: str, object_name: str, file: UploadFileSchema):
        await self.app.store.minio.client.put_object(
            bucket_name=bucket,
            object_name=object_name,
            data=file.file,
            length=file.size,
        )

    @exception_handler
    async def delete(self, bucket: str, object_name: str):
        await self.app.store.minio.client.remove_object(
            bucket_name=bucket,
            object_name=object_name,
        )

    @exception_handler
    async def download(self, bucket: str, object_name: str) -> StreamingResponse:
        session = self._session()
        try:
            response = await self.app.store.minio.client.get_object(
                bucket_name=bucket,
                object_name=object_name,
                session=session,
            )

            async def stream_iterator():
                async for chunk in response.content:
                    yield chunk
                await session.close()

            return StreamingResponse(
                content=stream_iterator(),
                headers=self._create_headers(object_name),
            )
        except Exception as e:
            await session.close()
            raise e

    @exception_handler
    async def is_object_exist(self, bucket: str, object_name: str) -> bool:
        await self.app.store.minio.client.stat_object(
            bucket_name=bucket,
            object_name=object_name,
        )
        return True

    @staticmethod
    def _session() -> aiohttp.ClientSession:
        return aiohttp.ClientSession()

    @staticmethod
    def _create_headers(filename: str) -> dict:
        return {
            "Content-Disposition": f"attachment filename={filename}",
            "Content-type": "image/jpeg",
        }
