import csv
from datetime import datetime, timedelta as td
from typing import Dict
from Card import Card
from CardManagerInterface import CardStorageInterface
import base64
from SyncInterface import SyncInterface
import io

class CardCsvStore(CardStorageInterface):
    def __init__(self, sync: SyncInterface, source: str, destination: str):
        self.sync = sync
        self.source = source
        self.destination = destination
        self.cards = {}
        self.load_cards()

    def save_cards(self) -> None:
        output = io.StringIO()
        writer = csv.writer(output)
        for card in self.cards.values():
            writer.writerow([
                card.key,
                CardCsvStore._encode_to_base64(card.name),
                card.status,
                card.interval.total_seconds() if card.interval else None,
                card.ease,
                card.step,
                card.timestamp.isoformat()
            ])
        self.sync.Push(self.destination, output.getvalue(), overwrite=True)

    def load_cards(self) -> None:                    
        data = self.sync.Pull(self.source)
        content = data.decode()
        csv_reader = csv.reader(io.StringIO(content))        
        for row in csv_reader:
            key = row[0]
            name = CardCsvStore._decode_from_base64(row[1])
            status = row[2]
            interval = td(seconds=float(row[3])) if row[3] else None
            ease = float(row[4])
            step = int(row[5])
            timestamp = datetime.fromisoformat(row[6])
            self.cards[name] = Card(name, key, status, interval, ease, step, timestamp)

    def add_card(self, card: Card) -> None:
        self.cards[card.name] = card

    def get_card(self, name: str) -> Card:
        return self.cards.get(name)

    def update_card(self, card: Card) -> None:
        if card.name in self.cards:
            self.cards[card.name] = card

    def delete_card(self, name: str) -> None:
        if name in self.cards:
            del self.cards[name]

    @staticmethod
    def _encode_to_base64(input_string: str) -> str:
        try:
            byte_data = input_string.encode('utf-8')
            base64_encoded = base64.b64encode(byte_data)
            return base64_encoded.decode('utf-8')
        except Exception as e:
            print(f"Error encoding to base64: {e}")
            return None
    
    @staticmethod
    def _decode_from_base64(base64_string: str) -> str:
        decoded_bytes = base64.b64decode(base64_string)
        return decoded_bytes.decode('utf-8')
