import boto3
from google.cloud import storage
from azure.storage.blob import BlobServiceClient
import logging

class CloudUploader:
    @staticmethod
    def upload_to_aws(file_path: str, config: dict) -> None:
        s3 = boto3.client(
            's3',
            aws_access_key_id=config['access_key'],
            aws_secret_access_key=config['secret_key'],
            region_name=config['region']
        )
        try:
            s3.upload_file(file_path, config['bucket_name'], file_path)
            logging.info(f"Successfully uploaded {file_path} to AWS S3 bucket {config['bucket_name']}.")
        except Exception as e:
            logging.error(f"Error uploading {file_path} to AWS S3: {e}")

    @staticmethod
    def upload_to_gcp(file_path: str, config: dict) -> None:
        try:
            client = storage.Client.from_service_account_json(config['service_account_key'])
            bucket = client.get_bucket(config['bucket_name'])
            blob = bucket.blob(file_path)
            blob.upload_from_filename(file_path)
            logging.info(f"Successfully uploaded {file_path} to GCP bucket {config['bucket_name']}.")
        except Exception as e:
            logging.error(f"Error uploading {file_path} to GCP: {e}")

    @staticmethod
    def upload_to_azure(file_path: str, config: dict) -> None:
        try:
            blob_service_client = BlobServiceClient.from_connection_string(config['connection_string'])
            blob_client = blob_service_client.get_blob_client(container=config['container_name'], blob=file_path)
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data)
            logging.info(f"Successfully uploaded {file_path} to Azure container {config['container_name']}.")
        except Exception as e:
            logging.error(f"Error uploading {file_path} to Azure: {e}")
