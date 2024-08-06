import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import getopt, sys
options = "acn:"
long_options = ["account", "container", "name", "file"]

def upload_blob(storage_account_name, container_name, blob_name, data, overwrite=True):
    account_url = f"https://{storage_account_name}.blob.core.windows.net"

    credential = DefaultAzureCredential()

    blob_service_client = BlobServiceClient(account_url=account_url, credential=credential)

    container_client = blob_service_client.get_container_client(container_name)

    try:
        container_client.create_container()

    except Exception as e:
        if "ContainerAlreadyExists" not in str(e):
            raise
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(data, overwrite=overwrite)
    print(f"Blob '{blob_name}' uploaded to container '{container_name}'.")
    

def upload_file(storage_account_name, container_name, blob_name, file_path):    
    with open(file_path, "rb") as data:
        upload_blob(storage_account_name, container_name, blob_name, data)

def download_blob(storage_account_name, container_name, blob_name):
    account_url = f"https://{storage_account_name}.blob.core.windows.net"
    credential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient(account_url=account_url, credential=credential)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)

    try:
        download_stream = blob_client.download_blob()
        blob_data = download_stream.readall()
        return blob_data
    except Exception as e:
        print(f"Failed to download blob '{blob_name}' from container '{container_name}': {e}")
        return None
    
def usage():
    print("Usage: azure_file_uploader.py [options] <file_path> <account_name> <container_name> <blob_name>")
    print("Options:")
    print("  -a, --account     Azure storage account name (defaults to env AZURE_STORAGE_ACCOUNT_NAME if not provided)")
    print("  -c, --container   Azure storage container name")
    print("  -b, --blob        Azure storage blob name")
    print("  -f, --file        File path")
    print("Positional Parameters (in order):")
    print("  <file_path> <account_name> <container_name> <blob_name>")

if __name__ == "__main__":

    account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
    container_name = None
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
            container_name = arg
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
            if container_name is None:
                container_name = args[2]
        if len(args) > 3:
            if blob_name is None:
                blob_name = args[3]

    if file_path is None:
        print("Error: file path is required.")
        usage()
        sys.exit(2)
    if blob_name is None:
        blob_name = os.path.basename(file_path)

    upload_file(account_name, container_name, blob_name, file_path)
