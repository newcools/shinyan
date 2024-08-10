from ShinyanCard import CardCsvStore
from backend.src.ShinyanCard.AzureBlobSync import AzureBlobSync
from Settings import load_settings_from_json

settings = load_settings_from_json('./config.json')
azure_blob_sync = AzureBlobSync(settings)
manager = CardCsvStore(azure_blob_sync, 'cards.csv', 'cards.csv')

from backend.src.ShinyanCard.Card import Card
from datetime import datetime, timezone

for name, card in manager.cards.items():
    print(f"{name} => {card.key}")
