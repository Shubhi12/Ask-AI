import boto3
from app.core.config import settings

client = None

def get_storage_client():
    global client
    if client is None:
        client = boto3.client(
            "s3",
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
            region_name=settings.S3_STORAGE_REGION or "ap-northeast-1",
        )
    return client