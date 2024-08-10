from pydantic import SecretStr
from pydantic_settings import BaseSettings
import json
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

class Settings(BaseSettings):
    storage_account_name: str
    container_name: str
    openai_key: SecretStr

    class Config:
        env_prefix = 'APP_'
        env_file = '.env'
        secrets_dir = '../secrets'

def load_settings_from_json(file_path: str, key_vault_name: str = None) -> Settings:
    with open(file_path, 'r') as f:
        config = json.load(f)
    
    blob_config = config['blob']
    openai_key_name = config['openai']['key_name']
    
    if key_vault_name:
        # Load OpenAI key from Azure Key Vault
        key_vault_url = f"https://{key_vault_name}.vault.azure.net/"
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=key_vault_url, credential=credential)
        secret = client.get_secret(openai_key_name)
        openai_key = secret.value
    else:
        # Load OpenAI key from a local secrets file
        openai_key_path = os.path.join(Settings.Config.secrets_dir, openai_key_name)
        with open(openai_key_path, 'r') as f:
            openai_key = f.read().strip()

    return Settings(
        storage_account_name=blob_config['storage_account_name'],
        container_name=blob_config['container_name'],
        openai_key=openai_key
    )
