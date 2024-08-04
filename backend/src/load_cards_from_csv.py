import CardCsvStore
from card import Card
from datetime import datetime, timedelta as td
import os

if __name__ == "__main__":
    print(os.getcwd())
    with open('./backend/assets/top3000japaneseword.txt', 'r', encoding='utf-8') as file:
        rows = file.readlines()

store = CardCsvStore.CardCsvStore()

rows = [row.strip() for row in rows]

for word in rows:
    print("start to process word: ", word)
    store.add_card(Card(word, datetime.now(), datetime.now() + td(days=1)))

store.save_cards()