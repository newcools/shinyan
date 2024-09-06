import json
import os
from typing import Optional, Dict
import re

from azure.appconfiguration import AzureAppConfigurationClient
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from pydantic_settings import BaseSettings


class BlobSettings(BaseSettings):
    storage_account_name: Optional[str]
    container_name: Optional[str]

class OpenAISettings(BaseSettings):
    api_key: Optional[str]

class Settings(BaseSettings):
    blob: Optional[BlobSettings]
    openai: Optional[OpenAISettings]

    class Config:
        env_file = ".env"
        extra = "allow"

app_config_name = os.getenv("APP_CONFIG_NAME")
local_config_path = os.getenv("LOCAL_CONFIG_PATH")
if not app_config_name:
    raise ValueError("APP_CONFIG_NAME environment variable is not set.")

app_config_endpoint = f"https://{app_config_name}.azconfig.io"
credential = DefaultAzureCredential()
client = AzureAppConfigurationClient(app_config_endpoint, credential)
keyvault_reference_pattern = re.compile(r'@Microsoft\.KeyVault\(SecretUri=(.+?)\)')

def parse_colon_delimited_keys(config: Dict[str, str]) -> Dict:
    parsed_config = {}
    for key, value in config.items():
        parts = key.split('__')
        d = parsed_config
        for part in parts[:-1]:
            if part not in d:
                d[part] = {}
            d = d[part]
        d[parts[-1]] = value
    return parsed_config


def load_config_from_azure() -> Dict:
    config_dict = {}
    for setting in client.list_configuration_settings():
        value = setting.value

        try:
            value_json = json.loads(value)
            if 'uri' in value_json:
                secret_value = load_secret_from_keyvault(value_json['uri'])
                config_dict[setting.key] = secret_value
            else:
                config_dict[setting.key] = value
        except json.JSONDecodeError:
            config_dict[setting.key] = value  # Regular string value, not a JSON

    return parse_colon_delimited_keys(config_dict)


def load_secret_from_keyvault(secret_uri: str) -> str:
    # Extract the Key Vault name from the URI
    vault_url = secret_uri.split("/secrets/")[0]

    # Create a Key Vault client
    secret_client = SecretClient(vault_url=vault_url, credential=credential)

    # Extract the secret name from the URI
    secret_name = secret_uri.split("/secrets/")[1].split("/")[0]

    # Retrieve the secret value
    secret = secret_client.get_secret(secret_name)
    return secret.value



def load_config_from_local() -> Dict:
    local_config_path = os.getenv("LOCAL_CONFIG_PATH")
    if local_config_path and os.path.exists(local_config_path):
        with open(local_config_path, 'r') as f:
            return json.load(f)
    return {}

def merge_configs(azure_config: Dict, local_config: Dict) -> Dict:
    for key, value in local_config.items():
        if isinstance(value, dict) and key in azure_config and isinstance(azure_config[key], dict):
            merge_configs(azure_config[key], value)
        else:
            azure_config[key] = value
    return azure_config


def load_config() -> Settings:
    azure_config = load_config_from_azure()
    local_config = load_config_from_local()
    merged_config = merge_configs(azure_config, local_config)
    return Settings(**merged_config)


settings = load_config()
