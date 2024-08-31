from datetime import datetime, timezone, timedelta
from unittest.mock import Mock, patch, PropertyMock

from src.ShinyanCard.Card import Card
from src.ShinyanCard.CardCsvStore import CardCsvStore
from src.ShinyanCard.CardManager import CardManager
from src.ShinyanCard.CardMasterLevel import CardMasterLevel
from src.ShinyanCard.CardStatus import CardStatus
from src.ShinyanCard.CardStorageInterface import CardStorageInterface


class TestCardManager:
    def test_next_card(self):
        timestamp = datetime.now(timezone.utc)
        mocked_card_store = Mock()
        mocked_card_store.cards = [
            Card(name="test1", status=CardStatus.RELEARNING, ease=3.0, step=0, timestamp=timestamp + timedelta(minutes=100)),
            Card(name="test2", status=CardStatus.RELEARNING, ease=3.0, step=0, timestamp=timestamp + timedelta(minutes=99)),
            Card(name="test3", status=CardStatus.RELEARNING, ease=3.0, step=0, timestamp=timestamp + timedelta(minutes=77)),
            Card(name="test4", status=CardStatus.RELEARNING, ease=3.0, step=0, timestamp=timestamp + timedelta(minutes=66)),
            Card(name="test5", status=CardStatus.RELEARNING, ease=3.0, step=0, timestamp=timestamp + timedelta(minutes=55))
        ]

        card_manager = CardManager(mocked_card_store)
        current_card = card_manager.next_card()
        assert current_card.name == mocked_card_store.cards[-1].name

        current_card.run(CardMasterLevel.EASY)
        current_card = card_manager.next_card()
        assert current_card.name == mocked_card_store.cards[-2].name

        current_card.run(CardMasterLevel.AGAIN)
        current_card = card_manager.next_card()
        assert current_card.name == mocked_card_store.cards[-2].name

        current_card.run(CardMasterLevel.GOOD)
        current_card = card_manager.next_card()
        assert current_card.name == mocked_card_store.cards[-3].name
