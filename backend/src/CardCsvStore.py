import csv
from datetime import datetime, timedelta as td
from typing import List
from card import Card
from persistence_interface import PersistenceInterface

class CardCsvStore(PersistenceInterface):
    def __init__(self, filename='cards.csv'):
        self.filename = filename

    def save_cards(self, cards: List[Card]) -> None:
        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            for card in cards:
                writer.writerow([
                    card.key,
                    card.status,
                    card.interval.total_seconds() if card.interval else None,
                    card.ease,
                    card.step,
                    card.timestamp.isoformat()
                ])

    def load_cards(self) -> List[Card]:
        cards = []
        try:
            with open(self.filename, 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    key = row[0]
                    interval = td(seconds=float(row[2])) if row[2] else None
                    timestamp = datetime.fromisoformat(row[5])
                    cards.append(Card(
                        key=key,
                        status=row[1],
                        interval=interval,
                        ease=float(row[3]),
                        step=int(row[4]),
                        timestamp=timestamp
                    ))
        except FileNotFoundError:
            pass
        return cards

    def add_card(self, card: Card) -> None:
        cards = self.load_cards()
        cards.append(card)
        self.save_cards(cards)

    def get_card(self, key: str) -> Card:
        cards = self.load_cards()
        for card in cards:
            if card.key == key:
                return card
        return None

    def update_card(self, card: Card) -> None:
        cards = self.load_cards()
        for i, existing_card in enumerate(cards):
            if existing_card.key == card.key:
                cards[i] = card
                break
        self.save_cards(cards)

    def delete_card(self, key: str) -> None:
        cards = self.load_cards()
        cards = [card for card in cards if card.key != key]
        self.save_cards(cards)