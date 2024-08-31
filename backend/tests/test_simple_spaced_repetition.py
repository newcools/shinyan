from datetime import timedelta, datetime
from src.ShinyanCard.Card import Card
from src.ShinyanCard.CardMasterLevel import CardMasterLevel
from src.ShinyanCard.CardStatus import CardStatus
from parameterized import parameterized

_minutes = lambda m: timedelta(minutes=m)
_days = lambda d: timedelta(days=d)


MINIMUM_EASE = 1.3
INITIAL_EASE = 2.5
AGAIN_EASE_DELTA = -0.2
HARD_EASE_DELTA = -0.15
EASY_EASE_DELTA = 0.15
HARD_INTERVAL = 1.2
EASY_INTERVAL_BONUS = 1.5

DUMMY_INITIAL_INTERVAL = timedelta(seconds=600)
DUMMY_INITIAL_EASE = 1.5

class TestSimpleSpacedRepetition:
    def test_new_card(self):
        card = Card("test")
        assert card.status == CardStatus.LEARNING
        assert card.step == 0
        assert card.interval is None
        assert card.ease == INITIAL_EASE

    @parameterized.expand([
        # learning
        (CardStatus.LEARNING, None, 111, 0, CardMasterLevel.AGAIN, CardStatus.LEARNING, timedelta(minutes=1), 111, 0),
        (CardStatus.LEARNING, None, 111, 0, CardMasterLevel.HARD, CardStatus.LEARNING, timedelta(minutes=6), 111, 1),
        (CardStatus.LEARNING, None, 111, 0, CardMasterLevel.GOOD, CardStatus.LEARNING, timedelta(minutes=10), 111, 1),
        (CardStatus.LEARNING, None, 111, 0, CardMasterLevel.EASY, CardStatus.REVIEWING, timedelta(4), 111, 1),
        (CardStatus.LEARNING, None, 111, 1, CardMasterLevel.GOOD, CardStatus.REVIEWING, timedelta(1), 111, 1), # step = 1
        # Reviewing
        (CardStatus.REVIEWING, DUMMY_INITIAL_INTERVAL, DUMMY_INITIAL_EASE, 1, CardMasterLevel.AGAIN, CardStatus.RELEARNING, timedelta(minutes=10), DUMMY_INITIAL_EASE - 0.2, 1),
        (CardStatus.REVIEWING, DUMMY_INITIAL_INTERVAL, DUMMY_INITIAL_EASE, 1, CardMasterLevel.HARD, CardStatus.REVIEWING, DUMMY_INITIAL_INTERVAL * 1.2, DUMMY_INITIAL_EASE - 0.15, 1),
        (CardStatus.REVIEWING, DUMMY_INITIAL_INTERVAL, DUMMY_INITIAL_EASE, 1, CardMasterLevel.GOOD, CardStatus.REVIEWING, DUMMY_INITIAL_INTERVAL * DUMMY_INITIAL_EASE, DUMMY_INITIAL_EASE, 1), # td x ease
        (CardStatus.REVIEWING, DUMMY_INITIAL_INTERVAL, DUMMY_INITIAL_EASE, 1, CardMasterLevel.EASY, CardStatus.REVIEWING, DUMMY_INITIAL_INTERVAL * DUMMY_INITIAL_EASE * 1.5, DUMMY_INITIAL_EASE + 0.15, 1),
        # relearning, ease has no affect to interval
        (CardStatus.RELEARNING, DUMMY_INITIAL_INTERVAL, DUMMY_INITIAL_EASE, 1, CardMasterLevel.AGAIN, CardStatus.RELEARNING, timedelta(minutes=1), DUMMY_INITIAL_EASE, 1),
        (CardStatus.RELEARNING, DUMMY_INITIAL_INTERVAL, DUMMY_INITIAL_EASE, 1, CardMasterLevel.HARD, CardStatus.RELEARNING, timedelta(minutes=6), DUMMY_INITIAL_EASE, 1),
        (CardStatus.RELEARNING, DUMMY_INITIAL_INTERVAL, DUMMY_INITIAL_EASE, 0, CardMasterLevel.GOOD, CardStatus.REVIEWING, timedelta(days=1), DUMMY_INITIAL_EASE, 0),
        (CardStatus.RELEARNING, DUMMY_INITIAL_INTERVAL, DUMMY_INITIAL_EASE, 1, CardMasterLevel.EASY, CardStatus.REVIEWING, timedelta(days=4), DUMMY_INITIAL_EASE, 1),
    ])
    def test_card_run(self,  status, interval, ease, step, level,
                      expected_status, expected_interval, expected_ease, expected_step):
        card = Card("test", status=status, interval=interval, ease=ease, step=step)
        card.run(level)
        assert card.status == expected_status, f"Expected status to be {expected_status}, but got {card.status}"
        assert card.interval == expected_interval, f"Expected interval to be {expected_interval}, but got {card.interval}"
        assert card.ease == expected_ease, f"Expected ease to be {expected_ease}, but got {card.ease}"
        assert card.step == expected_step, f"Expected step to be {expected_step}, but got {card.step}"

