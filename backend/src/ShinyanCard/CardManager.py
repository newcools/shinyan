import copy
import datetime
import json
from datetime import timedelta
from pathlib import Path
import random

from .AzureServices.SyncInterface import SyncInterface
from .Card import Card
from .CardContents import deserialize_card_contents, ContentType, ContentItemResource, serialize_card_contents
from .CardStorageInterface import CardStorageInterface
from .ContentGeneration.ContentGenerator import generate_contents
from .Settings import settings
from .ContentGeneration.speech_generator import generate_speech

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


    def next_card_resource(self) -> ContentItemResource:
        self.current_card = self.next_card()
        source_path = Path(self.current_card.key) / 'data.json'
        card_content = None
        card_json = self.sync.pull(source_path.as_posix())
        if card_json is not None:
            card_json = json.loads(card_json)
        else:
            card_json = generate_contents(self.current_card.name, "japanese")

        card_content = deserialize_card_contents(card_json)
        card_content.name = self.current_card.name
        card_content.key = self.current_card.key

        if len(card_content.contents) > 1:
            index = random.randint(0, len(card_content.contents) - 1)
            selected_content = card_content.contents[index]
            audio_resource = next((r for r in selected_content.resources if r.type == ContentType.AUDIO), None)
            if audio_resource is None:
                audio_path = Path(self.current_card.key) / str(index) / 'audio.mp3'
                audio = generate_speech(settings.openai.api_key, selected_content['Japanese'])
                self.sync.push(audio_path.as_posix(), audio)
                download_link = self.sync.get_download_link(audio_path.as_posix())
                audio_resource = ContentItemResource(type=ContentType.AUDIO, uri=download_link, extra={"last_update": datetime.UTC})
                selected_content.resources.append(audio_resource)
        else:
            raise ValueError("Content empty")
        self.sync.push(source_path.as_posix(), serialize_card_contents(card_content))

        return audio_resource

    def update(self, card: Card):
        self.data_source.update_card(card)
