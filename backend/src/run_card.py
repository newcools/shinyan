from CardCsvStore import CardCsvStore
from card import Card
from datetime import datetime, timedelta as td
if __name__ == "__main__":
    store = CardCsvStore()

    # Adding a new card
    new_card = Card(status="learning", interval=td(minutes=10), ease=2.0, step=1)
    store.add_card(new_card)

    # Retrieving a card
    card = store.get_card(0)
    print(card)

    # Updating the timestamp of the card when it is reviewed
    store.update_timestamp(0)

    # Retrieving the card again to see the updated timestamp
    card = store.get_card(0)
    print(card)

    # Updating a card's status
    if card:
        card.status = "reviewing"
        store.update_card(0, card)

    # Deleting a card
    store.delete_card(0)

    # Retrieving all cards
    cards = store.get_all_cards()
    for card in cards:
        print(card)
