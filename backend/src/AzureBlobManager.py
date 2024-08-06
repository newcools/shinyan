from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

class AzureBlobManager:
    def __init__(self, storage_account_name, container_name):
        self.storage_account_name = storage_account_name
        self.container_name = container_name
        self.account_url = f"https://{storage_account_name}.blob.core.windows.net"
        self.credential = DefaultAzureCredential()
        self.blob_service_client = BlobServiceClient(account_url=self.account_url, credential=self.credential)
        self.container_client = self.blob_service_client.get_container_client(container_name)

    def upload_blob(self, blob_name, data, overwrite=True):
        try:
            self.container_client.create_container()
        except Exception as e:
            if "ContainerAlreadyExists" not in str(e):
                raise

        blob_client = self.container_client.get_blob_client(blob_name)
        try:
            blob_client.upload_blob(data, overwrite=overwrite)
            print(f"Blob '{blob_name}' uploaded to container '{self.container_name}'.")
        except Exception as e:
            raise

    def upload_file(self, blob_name, file_path):
        with open(file_path, "rb") as data:
            self.upload_blob(blob_name, data)

    def download_blob(self, blob_name):
        blob_client = self.container_client.get_blob_client(blob_name)
        try:
            download_stream = blob_client.download_blob()
            blob_data = download_stream.readall()
            return blob_data
        except Exception as e:
            print(f"Failed to download blob '{blob_name}' from container '{self.container_name}': {e}")
            return None

    def download_file(self, blob_name, file_path):
        blob_client = self.container_client.get_blob_client(blob_name)
        try:
            with open(file_path, "wb") as file:
                download_stream = blob_client.download_blob()
                file.write(download_stream.readall())
            print(f"Blob '{blob_name}' downloaded to '{file_path}'.")
        except Exception as e:
            print(f"Failed to download blob '{blob_name}' from container '{self.container_name}': {e}")