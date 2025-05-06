# utils/s3.py
import boto3
import uuid
from core.config import settings


# S3操作するための設定
# s3_client = boto3.client(
#     "s3",
#     aws_access_key_id=settings.aws_access_key_id,
#     aws_secret_access_key=settings.aws_secret_access_key,
#     region_name=settings.aws_region
# )

def upload_to_s3(
    file_bytes: bytes,
    filename: str,
    content_type: str
)->str:
    key = f"generated/{uuid.uuid4()}_{filename}"
    s3_client.put_object(
        Bucket=settings.aws_s3_bucket_name,
        Key=key,
        Body=file_bytes,
        ContentType=content_type,
        ACL="public-read"
    )
    return f"https://{settings.aws_s3_bucket_name}.s3.{settings.aws_region}.amazonaws.com/{key}"