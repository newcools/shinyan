import json
from pathlib import Path
from random import random

from .Card import Card
from .CardStorageInterface import CardStorageInterface
from datetime import timedelta
import copy
from .ContentGeneration.ContentGenerator import generate_contents
from .AzureServices.SyncInterface import SyncInterface
from .Settings import settings


class CardManager:
    def __init__(self, data_source: CardStorageInterface, sync_service: SyncInterface):
        self.data_source = data_source
        self.sync = sync_service
        self._cards = copy.deepcopy(data_source.cards)
        self.current_card = None

    @property
    def sorted_cards(self):
        return sorted(self._cards, key=lambda c: c.timestamp + (c.interval or timedelta(0)))

    def next_card(self) -> Card:
        if self._cards:
            return self.sorted_cards[0]
        else:
            raise ValueError("No card.")
    def next_card_ex(self):
        self.current_card = self.next_card()
        source_path = Path(self.current_card.key) / 'data.json'
        examples_data = None
        examples_content = self.sync.pull(source_path.as_posix())
        if examples_content is not None:
            examples_data = json.loads(examples_content)
        else:
            examples_data = generate_example_sentences(settings.openai_key.get_secret_value(),
                                                       self.current_card.name,
                                                       "japanese")
            self.sync.push(source_path.as_posix(), json.dumps(examples_data))

        examples_items = examples_data['examples']
        if len(examples_items) > 1:
            index = random.randint(0, len(examples_items) - 1)
            example = examples_items[index]
            audio_path = Path(self.current_card.key) / str(index) / 'audio.mp3'
            audio = self.sync.pull(audio_path.as_posix())
            if audio is None:
                from src.ShinyanCard.ContentGeneration.speech_generator import generate_speech
                audio = generate_speech(settings.openai_key.get_secret_value(), example['Japanese'])
                self.sync.push(audio_path.as_posix(), audio)
            download_link = self.sync.get_download_link(audio_path.as_posix())
            print(download_link)
            print(example['English'])
            print(example['Japanese'])
            print(example['Hiragana'])

    def update(self, card: Card):
        self.data_source.update_card(card)
