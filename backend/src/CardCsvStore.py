import csv
from datetime import datetime, timedelta as td
from typing import List
from Card import Card
from CardManagerInterface import CardManagerInterface
import base64
from SyncInterface import SyncInterface
import io

class CardCsvStore(CardManagerInterface):
    def __init__(self, sync: SyncInterface, source: str, destination: str):
        self.sync = sync
        self.source = source
        self.destination = destination
        self.cards = []
        all_cards = self.load_cards()
        self.cards = {card.name: card for card in all_cards}

    def save_cards(self) -> None:
        output = io.StringIO()
        writer = csv.writer(output)
        for card in self.cards:
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

    def load_cards(self):                    
        data = self.sync.Pull(self.source)
        content = data.decode()
        csv_reader = csv.reader(io.StringIO(content))        
        for row in csv_reader:
            key = row[0]
            name = CardCsvStore._decode_from_base64(row[1])
            status = row[2]
            interval = td(seconds=float(row[3])) if row[3] else None
            ease = float(row[4])
            step=int(row[5])
            timestamp = datetime.fromisoformat(row[6])
            self.cards.append(Card(name, key, status, interval, ease, step, timestamp))


    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def get_card(self, key: str) -> Card:
        for card in self.cards:
            if card.key == key:
                return card
        return None

    def update_card(self, card: Card) -> None:
        for i, existing_card in enumerate(self.cards):
            if existing_card.key == card.key:
                self.cards[i] = card
                break

    def delete_card(self, key: str) -> None:
        cards = self.load_cards()
        cards = [card for card in cards if card.key != key]

    @staticmethod
    def _encode_to_base64(input_string: str) -> str:
        try:
            # Ensure the string is in a consistent Unicode format
            if isinstance(input_string, str):
                # If the input is already a string, encode it to bytes using UTF-8
                byte_data = input_string.encode('utf-8')
            else:
                # If the input is not a string, try converting it to a string
                byte_data = str(input_string).encode('utf-8')
    
            # Encode the bytes using base64
            base64_encoded = base64.b64encode(byte_data)
            # Convert the base64 bytes back to a string
            return base64_encoded.decode('utf-8')
        except Exception as e:
            print(f"Error encoding to base64: {e}")
            return None
    
    @staticmethod
    def _decode_from_base64(base64_string: str) -> str:
        decoded_bytes = base64.b64decode(base64_string)
        return decoded_bytes.decode('utf-8')