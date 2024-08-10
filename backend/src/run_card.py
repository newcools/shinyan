from CardCsvStore import CardCsvStore
from AzureBlobSync import AzureBlobSync
from Settings import load_settings_from_json

settings = load_settings_from_json('./config.json')
azure_blob_sync = AzureBlobSync(settings)
manager = CardCsvStore(azure_blob_sync, 'cards.csv', 'cards.csv')

from Card import Card
from datetime import datetime, timezone

allCards = manager.get_all_cards()
