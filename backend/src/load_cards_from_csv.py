import CardCsvStore
from Card import Card
from datetime import datetime, timedelta as td
import os

if __name__ == "__main__":
    with open('./backend/assets/top3000japaneseword.txt', 'r', encoding='utf-8') as file:
       rows = file.readlines()

    store = CardCsvStore.CardCsvStore('./backend/assets/cards.csv')
    
    rows = [row.strip() for row in rows]
    
    for word in rows:
       print("start to process word: ", word)
       store.add_card(Card(word))
    store.save_cards()
    
    print("===================loaded begin ======================")
    for word in store.cards:
        print(word.name)
        # print(word.status)
        # print(word.interval)
        # print(word.ease)
        # print(word.step)
        # print(word.timestamp)
    print("===================loaded end ======================")