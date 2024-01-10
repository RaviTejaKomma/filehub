from google.cloud import storage
import os
import datetime


class GCSHandler:
    def __init__(self, credentials_path, logger):
        self.client = storage.Client.from_service_account_json(credentials_path)
        self.logger = logger

    def upload_blob(self, bucket_name, local_file_path, dest_blob_name):
        try:
            bucket = self.client.bucket(bucket_name)

            # Upload local file to the GCS bucket
            blob = bucket.blob(dest_blob_name)
            blob.upload_from_filename(local_file_path)
            self.logger.info(f"Successfully uploaded the blob {dest_blob_name} to bucket {bucket_name}")
        except Exception as e:
            self.logger.error(f"Exception occurred while uploading blob to bucket {bucket_name} with error: {str(e)}")
            raise
        finally:
            os.remove(local_file_path)

    def download_blob(self, bucket_name, src_blob_name, dest_file_name):
        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(src_blob_name)
            blob.download_to_filename(dest_file_name)
            self.logger.info(f"Successfully downloaded the blob {src_blob_name} to {dest_file_name}")
        except Exception as e:
            self.logger.error(f"Exception occurred while downloading blob {src_blob_name} with error: {str(e)}")
            raise

    def generate_download_signed_url(self, bucket_name, blob_name, desired_filename):
        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(blob_name)

            signed_url = blob.generate_signed_url(
                version="v4",
                # URL will be valid for 15 minutes
                expiration=datetime.timedelta(minutes=15),
                # Allow only GET requests using this URL
                method="GET",
                response_disposition=f"attachment; filename={desired_filename}",
            )
        except Exception as e:
            self.logger.error(
                f"Exception occurred while generating signed_url for blob {blob_name} with error: {str(e)}")
            raise
        return signed_url

    def delete_blob(self, bucket_name, blob_name):
        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            blob.delete()
            self.logger.info(f"Successfully deleted blob {blob_name} from {bucket_name}")
        except Exception as e:
            self.logger.error(f"Exception occurred while deleting blob {blob_name} with error: {str(e)}")
            raise
