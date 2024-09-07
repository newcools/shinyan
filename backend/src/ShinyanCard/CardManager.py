import copy
import datetime
import io
import json
import random
from datetime import timedelta, datetime
from pathlib import Path

from .AzureServices.SyncInterface import SyncInterface
from .Card import Card
from .CardContents import custom_decoder, ContentType, ContentItemResource, BaseContentItem, CustomEncoder
from .CardStorageInterface import CardStorageInterface
from .ContentGeneration.ContentGenerator import generate_contents
from .ContentGeneration.speech_generator import generate_speech


class CardManager:
    def __init__(self, data_source: CardStorageInterface, sync_service: SyncInterface):
        self.data_source = data_source
        self.sync = sync_service
        self._cards = copy.deepcopy(data_source.cards)
        self._current_card = None

    @property
    def sorted_cards(self):
        return sorted(self._cards, key=lambda c: c.timestamp + (c.interval or timedelta(0)))

    @property
    def current_card(self) -> Card:
        return self._current_card

    def next_card(self) -> Card:
        if self._cards:
            return self.sorted_cards[0]
        else:
            raise ValueError("No card.")

    def next_card_content(self) -> BaseContentItem:
        self._current_card = self.next_card()
        source_path = Path(self.current_card.key) / 'data.json'
        card_content = None
        card_json = self.sync.pull(source_path.as_posix())
        if card_json is not None:
            card_json = json.loads(card_json)
        else:
            card_json = generate_contents(self.current_card.name, "japanese")

        card_content = custom_decoder(card_json)
        card_content.name = self.current_card.name
        card_content.key = self.current_card.key

        if len(card_content.contents) > 1:
            index = random.randint(0, len(card_content.contents) - 1)
            selected_content = card_content.contents[index]
            audio_resource = next((r for r in selected_content.resources if r.type == ContentType.AUDIO), None)
            if audio_resource is None:
                audio_path = Path(self.current_card.key) / str(index) / 'audio.mp3'
                audio = generate_speech(selected_content.text)
                self.sync.push(audio_path.as_posix(), audio)
                download_link = self.sync.get_download_link(audio_path.as_posix())
                audio_resource = ContentItemResource(type=ContentType.AUDIO, uri=download_link,
                                                     extra={"last_update": datetime.utcnow()})
                selected_content.resources.append(audio_resource)
        else:
            raise ValueError("Content empty")
        memory_file = io.BytesIO()
        json_data = json.dumps(card_content, cls=CustomEncoder, ensure_ascii=False)
        memory_file.write(json_data.encode('utf-8'))
        memory_file.seek(0)
        self.sync.push(source_path.as_posix(), memory_file)
        return selected_content

    def update(self, card: Card):
        self.data_source.update_card(card)
