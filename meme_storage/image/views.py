from typing import Any
from uuid import uuid4

from core.app import Request
from fastapi import APIRouter, Form

from .schemas import OkSchema, UploadFileSchema

image_route = APIRouter()


@image_route.post(
    "/upload",
    response_model=OkSchema,
)
async def upload_image(
        request: "Request",
        file: UploadFileSchema,
        bucket: str = Form(),
        object_name: str = Form(),
) -> Any:
    print(bucket, object_name, file)
    await request.app.store.s3.upload(bucket, object_name, file)
    return OkSchema()


@image_route.get("/download/{bucket}/{object_name}")
async def download(request: "Request", bucket: str, object_name: str) -> Any:
    return await request.app.store.s3.download(bucket, object_name)


@image_route.delete(
    "/delete/{bucket}/{object_name}",
    response_model=OkSchema,
)
async def delete(request: "Request", bucket: str, object_name: str) -> Any:
    await request.app.store.s3.is_object_exist(bucket, object_name)
    await request.app.store.s3.delete(bucket, object_name)
    return OkSchema()


@image_route.put(
    "/update/{bucket}/{object_name}",
    response_model=OkSchema,
)
async def update(
        request: "Request",
        bucket: str,
        object_name: str,
        file: UploadFileSchema,
) -> Any:
    await request.app.store.s3.is_object_exist(bucket, object_name)
    await request.app.store.s3.upload(bucket, object_name, file)
    return OkSchema()
