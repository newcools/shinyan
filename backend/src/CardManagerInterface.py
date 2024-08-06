from abc import ABC, abstractmethod
from typing import List
from Card import Card

class CardManagerInterface(ABC):
    @abstractmethod
    def save_cards(self, cards: List[Card]) -> None:
        pass

    @abstractmethod
    def load_cards(self) -> List[Card]:
        pass

    @abstractmethod
    def add_card(self, card: Card) -> None:
        pass

    @abstractmethod
    def get_card(self, key: str) -> Card:
        pass

    @abstractmethod
    def update_card(self, card: Card) -> None:
        pass

    @abstractmethod
    def delete_card(self, key: str) -> None:
        pass
