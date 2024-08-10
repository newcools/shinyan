from typing import List
from Card import Card
from datetime import timezone, datetime
from CardManagerInterface import CardManagerInterface
from SyncInterface import SyncInterface

class CardManager(CardManagerInterface):
    def __init__(self, sync: SyncInterface, source: str, destination: str):
        self.sync = sync
        self.source = source
        self.destination = destination
        all_cards = self.load_cards()
        self.cards = {card.key: card for card in all_cards}

    def save_cards(self, cards: List[Card]) -> None:
        self.sync.Push(self.destination, cards, overwrite=True)

    def load_cards(self) -> List[Card]:
        return self.sync.Pull(self.source)

    def add_card(self, card: Card) -> None:
        self.cards[card.key] = card
        self.save_cards(list(self.cards.values()))

    def get_card(self, key: str) -> Card:
        return self.cards.get(key)

    def update_card(self, card: Card) -> None:
        if card.key in self.cards:
            self.cards[card.key] = card
            self.save_cards(list(self.cards.values()))

    def delete_card(self, key: str) -> None:
        if key in self.cards:
            del self.cards[key]
            self.save_cards(list(self.cards.values()))

    def get_all_cards(self) -> List[Card]:
        return list(self.cards.values())

    def update_timestamp(self, key: str) -> None:
        if key in self.cards:
            self.cards[key].timestamp = datetime.now(timezone.utc)
            self.save_cards(list(self.cards.values()))

    def next_card(self) -> Card:
        return list(self.cards.values())[0]
