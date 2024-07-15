import os
import logging
import boto3
from google.cloud import storage
from azure.storage.blob import BlobServiceClient

def upload_to_aws(directory: str, config: dict) -> None:
    """Uploads files to AWS S3."""
    s3 = boto3.client(
        's3',
        aws_access_key_id=config.get('access_key_id'),
        aws_secret_access_key=config.get('secret_access_key'),
        region_name=config.get('region')
    )
    bucket_name = config.get('bucket_name', 'mg-miner-results')

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            s3_key = os.path.relpath(file_path, directory)
            s3.upload_file(file_path, bucket_name, s3_key)
            logging.info(f"Uploaded {file_path} to s3://{bucket_name}/{s3_key}")

def upload_to_gcp(directory: str, config: dict) -> None:
    """Uploads files to Google Cloud Storage."""
    client = storage.Client.from_service_account_json(config.get('credentials'))
    bucket_name = config.get('bucket_name', 'mg-miner-results')
    bucket = client.bucket(bucket_name)

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            blob = bucket.blob(os.path.relpath(file_path, directory))
            blob.upload_from_filename(file_path)
            logging.info(f"Uploaded {file_path} to gs://{bucket_name}/{blob.name}")

def upload_to_azure(directory: str, config: dict) -> None:
    """Uploads files to Azure Blob Storage."""
    blob_service_client = BlobServiceClient.from_connection_string(config.get('connection_string'))
    container_name = config.get('container_name', 'mg-miner-results')

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=os.path.relpath(file_path, directory))
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data)
            logging.info(f"Uploaded {file_path} to {container_name}/{os.path.relpath(file_path, directory)}")
