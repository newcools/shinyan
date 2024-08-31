import json
import random
from pathlib import Path

from ShinyanCard.CardCsvStore import CardCsvStore
from ShinyanCard.AzureServices.AzureBlobSync import AzureBlobSync
from ShinyanCard.Settings import settings
from ShinyanCard.CardManager import CardManager
from ShinyanCard.ContentGeneration.ContentGenerator import generate_contents
from ShinyanCard.ContentGeneration.speech_generator import generate_speech
azure_blob_sync = AzureBlobSync(settings.storage_account_name, settings.container_name)
card_store = CardCsvStore(azure_blob_sync, 'cards.csv', 'cards.csv')
card_manager = CardManager(card_store)

current_card = card_manager.next_card()
source_path = Path(current_card.key) / 'examples.json'
examples_data = None
examples_content = azure_blob_sync.pull(source_path.as_posix())
if examples_content is not None:
    examples_data = json.loads(examples_content)
else:
    examples_data = generate_contents(settings.openai_key.get_secret_value(), current_card.name, "japanese")
    azure_blob_sync.push(source_path.as_posix(), json.dumps(examples_data))

examples_items = examples_data['examples']
if len(examples_items) > 1:
    index = random.randint(0, len(examples_items) - 1)
    example = examples_items[index]
    audio_path = Path(current_card.key) / str(index) / 'audio.mp3'
    audio = azure_blob_sync.pull(audio_path.as_posix())
    if audio is None:
        audio = generate_speech(settings.openai_key.get_secret_value(), example['Japanese'])
        azure_blob_sync.push(audio_path.as_posix(), audio)
    download_link = azure_blob_sync.get_download_link(audio_path.as_posix())
    print(download_link)
    print(example['English'])
    print(example['Japanese'])
    print(example['Hiragana'])






