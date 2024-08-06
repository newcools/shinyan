from pydantic import BaseSettings, SecretStr
import json

class Settings(BaseSettings):
    storage_account_name: str
    storage_account_key: SecretStr
    container_name: str
    blob_name: str
    file_path: str

    class Config:
        env_prefix = 'APP_'
        env_file = '.env'
        secrets_dir = '/path/to/secrets'  # Optional: Directory for secrets

def load_settings_from_json(file_path: str) -> Settings:
    with open(file_path, 'r') as f:
        config = json.load(f)
    return Settings(**config['azure'], **config['blob'])