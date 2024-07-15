import unittest
from unittest.mock import patch, MagicMock
from mg_miner.core.cloud_upload import CloudUploader

class TestCloudUploader(unittest.TestCase):

    @patch('boto3.client')
    def test_upload_to_aws(self, mock_boto_client):
        mock_s3 = mock_boto_client.return_value
        config = {
            'bucket_name': 'test-bucket',
            'access_key': 'test-access-key',
            'secret_key': 'test-secret-key',
            'region': 'test-region'
        }
        CloudUploader.upload_to_aws('test_file.txt', config)
        mock_s3.upload_file.assert_called_with('test_file.txt', 'test-bucket', 'test_file.txt')

    @patch('google.cloud.storage.Client')
    def test_upload_to_gcp(self, mock_storage_client):
        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        mock_storage_client.return_value.get_bucket.return_value = mock_bucket
        mock_bucket.blob.return_value = mock_blob
        config = {
            'bucket_name': 'test-bucket',
            'service_account_key': 'path-to-key.json'
        }
        CloudUploader.upload_to_gcp('test_file.txt', config)
        mock_blob.upload_from_filename.assert_called_with('test_file.txt')

    @patch('azure.storage.blob.BlobServiceClient')
    def test_upload_to_azure(self, mock_blob_service_client):
        mock_blob_client = MagicMock()
        mock_blob_service_client.from_connection_string.return_value.get_blob_client.return_value = mock_blob_client
        config = {
            'container_name': 'test-container',
            'connection_string': 'test-connection-string'
        }
        CloudUploader.upload_to_azure('test_file.txt', config)
        mock_blob_client.upload_blob.assert_called()

if __name__ == '__main__':
    unittest.main()
