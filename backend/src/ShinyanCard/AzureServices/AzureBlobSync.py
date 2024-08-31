from abc import ABC

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from .SyncInterface import SyncInterface
from typing import Union
from datetime import datetime, timedelta, timezone


class AzureBlobSync(SyncInterface, ABC):
    def __init__(self, storage_account_name, container_name):
        self.storage_account_name = storage_account_name
        self.container_name = container_name
        self.account_url = f"https://{storage_account_name}.blob.core.windows.net"
        self.credential = DefaultAzureCredential()
        self.blob_service_client = BlobServiceClient(account_url=self.account_url, credential=self.credential)
        self.container_client = self.blob_service_client.get_container_client(container_name)

    def push(self, destination: str, data, force: bool = True):
        try:
            self.container_client.create_container()
        except Exception as e:
            if "ContainerAlreadyExists" not in str(e):
                raise

        blob_client = self.container_client.get_blob_client(destination)
        try:
            blob_client.upload_blob(data, overwrite=force)
            print(f"Blob '{destination}' uploaded to container '{self.container_name}'.")
        except Exception as e:
            raise

    def pull(self, source: str) -> Union[bytes, None]:
        blob_client = self.container_client.get_blob_client(source)
        try:
            download_stream = blob_client.download_blob()
            blob_data = download_stream.readall()
            return blob_data
        except Exception as e:
            print(f"Failed to download blob '{source}' from container '{self.container_name}': {e}")
            return None

    def get_download_link(self, blob_name: str) -> str:
        delegation_key_start_time = datetime.now(timezone.utc)
        delegation_key_expiry_time = delegation_key_start_time + timedelta(days=1)

        user_delegation_key = self.blob_service_client.get_user_delegation_key(
            key_start_time=delegation_key_start_time,
            key_expiry_time=delegation_key_expiry_time
        )
        sas_token = generate_blob_sas(
            account_name=self.blob_service_client.account_name,
            container_name=self.container_name,
            blob_name=blob_name,
            user_delegation_key=user_delegation_key,
            permission=BlobSasPermissions(read=True),
            start=delegation_key_start_time,
            expiry=delegation_key_expiry_time
        )
        return f"https://{self.blob_service_client.account_name}.blob.core.windows.net/{self.container_name}/{blob_name}?{sas_token}"
