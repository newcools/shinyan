from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from Settings import Settings
from SyncInterface import SyncInterface

class AzureBlobSync(SyncInterface):
    def __init__(self, settings: Settings):
        self.storage_account_name = settings.storage_account_name
        self.storage_account_key = settings.storage_account_key.get_secret_value()
        self.container_name = settings.container_name
        self.account_url = f"https://{settings.storage_account_name}.blob.core.windows.net"
        self.credential = DefaultAzureCredential()
        self.blob_service_client = BlobServiceClient(account_url=self.account_url, credential=self.credential)
        self.container_client = self.blob_service_client.get_container_client(settings.container_name)

    def Push(self, destination: str, data, overwrite: bool = True):
        try:
            self.container_client.create_container()
        except Exception as e:
            if "ContainerAlreadyExists" not in str(e):
                raise

        blob_client = self.container_client.get_blob_client(destination)
        try:
            blob_client.upload_blob(data, overwrite=overwrite)
            print(f"Blob '{destination}' uploaded to container '{self.container_name}'.")
        except Exception as e:
            raise

    def Pull(self, source: str):
        blob_client = self.container_client.get_blob_client(source)
        try:
            download_stream = blob_client.download_blob()
            blob_data = download_stream.readall()
            return blob_data
        except Exception as e:
            print(f"Failed to download blob '{source}' from container '{self.container_name}': {e}")
            return None