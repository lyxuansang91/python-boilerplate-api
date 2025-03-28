import logging

import boto3

from app.core.config import settings

logger = logging.getLogger(__name__)

class S3Client:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        self.bucket_name = settings.BUCKET

    def upload_file(self, file_path: str, s3_key: str, content_type: str | None = None) -> str:
        """
        Upload file to S3 and return the URL
        """
        try:
            extra_args = {}
            if content_type:
                extra_args['ContentType'] = content_type

            self.s3_client.upload_file(
                file_path,
                self.bucket_name,
                s3_key,
                ExtraArgs=extra_args
            )
            url = f"https://{self.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{s3_key}"
            logger.info(f"Successfully uploaded file to {url}")
            return url
        except Exception as e:
            logger.error(f"Error uploading file to S3: {str(e)}")
            raise

    def download_file(self, s3_key: str, local_path: str) -> None:
        """
        Download file from S3
        """
        try:
            self.s3_client.download_file(self.bucket_name, s3_key, local_path)
            logger.info(f"Successfully downloaded file from S3: {s3_key}")
        except Exception as e:
            logger.error(f"Error downloading file from S3: {str(e)}")
            raise

    def delete_file(self, s3_key: str) -> None:
        """
        Delete file from S3
        """
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
            logger.info(f"Successfully deleted file from S3: {s3_key}")
        except Exception as e:
            logger.error(f"Error deleting file from S3: {str(e)}")
            raise
