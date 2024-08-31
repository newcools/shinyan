import os
import sys
import getopt
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient


class AzureBlobClient:
    def __init__(self, storage_account_name: str, container_name: str):
        self.storage_account_name = storage_account_name
        self.container_name = container_name
        self.account_url = f"https://{storage_account_name}.blob.core.windows.net"
        self.credential = DefaultAzureCredential()
        self.blob_service_client = BlobServiceClient(account_url=self.account_url, credential=self.credential)
        self.container_client = self._get_or_create_container(container_name)

    def _get_or_create_container(self, container_name: str) -> ContainerClient:
        container_client = self.blob_service_client.get_container_client(container_name)
        try:
            container_client.create_container()
            print(f"Created new container: {container_name}")
        except Exception as e:
            if "ContainerAlreadyExists" in str(e):
                print(f"Container {container_name} already exists.")
            else:
                raise e
        return container_client

    def upload_blob(self, blob_name: str, data, overwrite: bool = True):
        blob_client = self.container_client.get_blob_client(blob_name)
        blob_client.upload_blob(data, overwrite=overwrite)
        print(f"Blob '{blob_name}' uploaded to container '{self.container_name}'.")

    def upload_file(self, blob_name: str, file_path: str, overwrite: bool = True):
        with open(file_path, "rb") as data:
            self.upload_blob(blob_name, data, overwrite=overwrite)

    def download_blob(self, blob_name: str) -> bytes:
        blob_client = self.container_client.get_blob_client(blob_name)
        try:
            download_stream = blob_client.download_blob()
            blob_data = download_stream.readall()
            print(f"Blob '{blob_name}' downloaded from container '{self.container_name}'.")
            return blob_data
        except Exception as e:
            print(f"Failed to download blob '{blob_name}': {e}")
            return None


def usage():
    print("Usage: azure_file_uploader.py [options] <file_path> <account_name> <container_name> <blob_name>")
    print("Options:")
    print("  -a, --account     Azure storage account name (defaults to env AZURE_STORAGE_ACCOUNT_NAME if not provided)")
    print("  -c, --container   Azure storage container name")
    print("  -b, --blob        Azure storage blob name")
    print("  -f, --file        File path")


if __name__ == "__main__":
    account_name = None
    blob_container_name = None
    blob_name = None
    file_path = None

    try:
        opts, args = getopt.getopt(sys.argv[1:], "a:c:b:f:", ["account=", "container=", "blob=", "file="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-a", "--account"):
            account_name = arg
        elif opt in ("-c", "--container"):
            blob_container_name = arg
        elif opt in ("-b", "--blob"):
            blob_name = arg
        elif opt in ("-f", "--file"):
            file_path = arg

    if len(args) > 0:
        if file_path is None:
            file_path = args[0]
        if len(args) > 1:
            if account_name is None:
                account_name = args[1]
        if len(args) > 2:
            if blob_container_name is None:
                blob_container_name = args[2]
        if len(args) > 3:
            if blob_name is None:
                blob_name = args[3]

    if file_path is None:
        print("Error: file path is required.")
        usage()
        sys.exit(2)

    if blob_name is None:
        blob_name = os.path.basename(file_path)

    # Initialize the AzureBlobClient with the provided account and container names
    blob_client = AzureBlobClient(storage_account_name=account_name, container_name=blob_container_name)

    # Upload the file to Azure Blob Storage
    blob_client.upload_file(blob_name=blob_name, file_path=file_path)
