from typing import List
from Card import Card
from persistence_interface import PersistenceInterface
from datetime import timezone, datetime

class CardManager:
    def __init__(self, persistence: PersistenceInterface):
        self.persistence = persistence
        self.cards = {card.key: card for card in self.persistence.load_cards()}

    def add_card(self, card: Card) -> None:
        self.cards[card.key] = card
        self.persistence.save_cards(list(self.cards.values()))

    def get_card(self, key: str) -> Card:
        return self.cards.get(key)

    def update_card(self, card: Card) -> None:
        if card.key in self.cards:
            self.cards[card.key] = card
            self.persistence.save_cards(list(self.cards.values()))

    def delete_card(self, key: str) -> None:
        if key in self.cards:
            del self.cards[key]
            self.persistence.save_cards(list(self.cards.values()))

    def get_all_cards(self) -> List[Card]:
        return list(self.cards.values())

    def update_timestamp(self, key: str) -> None:
        if key in self.cards:
            self.cards[key].timestamp = datetime.now(timezone.utc)
            self.persistence.save_cards(list(self.cards.values()))

    def next_card(self) -> None:
        return list(self.cards.values())[0]