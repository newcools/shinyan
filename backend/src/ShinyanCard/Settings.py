from pathlib import Path

from pydantic import SecretStr, BaseModel
import json
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


class Settings(BaseModel):
    storage_account_name: str
    container_name: str
    openai_key: SecretStr

    class Config:
        env_prefix = 'APP_'
        env_file = '../.env'
        secrets_dir = Path(__file__).parent.parent / 'secrets'


def load_settings_from_json(file_path: str) -> Settings:
    with open(file_path, 'r') as f:
        config = json.load(f)

    blob_config = config['blob']
    key_vault_name = config.get('key_vault_name')
    openai_key_name = config['openai']['key_name']

    if key_vault_name:
        key_vault_url = f"https://{key_vault_name}.vault.azure.net/"
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=key_vault_url, credential=credential)
        secret = client.get_secret(openai_key_name)
        openai_key = secret.value
    else:
        openai_key_path = Path(Settings.Config.secrets_dir) / openai_key_name
        with open(openai_key_path, 'r') as f:
            openai_key = f.read().strip()

    return Settings(
        storage_account_name=blob_config['storage_account_name'],
        container_name=blob_config['container_name'],
        openai_key=openai_key,
        # _env_file=settings.Config.env_file,
        # _secrets_dir=settings.Config.secrets_dir,
    )


config_json_path = './config.json'
settings = load_settings_from_json(config_json_path)
