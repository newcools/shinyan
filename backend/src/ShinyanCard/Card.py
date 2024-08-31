from datetime import timezone, datetime, timedelta as td
from .CardStatus import CardStatus
from .CardMasterLevel import CardMasterLevel
import uuid


class Card:
    def __init__(self, name, key=None, status: CardStatus = CardStatus.LEARNING, interval=None, ease: float = 2.5,
                 step=0, timestamp=None):
        if key is None:
            self._id = uuid.uuid4().hex
        else:
            self._id = key
        self._name = name
        self.status = status
        self.interval = interval
        self.ease = max(ease, 1.3)
        self.step = step
        self.timestamp = timestamp or datetime.now(timezone.utc)

    @property
    def key(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def due(self):
        return self.timestamp if self.interval is None else self.timestamp + self.interval

    def __repr__(self):
        return f"Card(status={self.status}, step={self.step}, interval={self.interval}, ease={self.ease}, timestamp={self.timestamp}, due={self.due})"

    def run(self, level: CardMasterLevel):
        run_options = []
        if self.status == CardStatus.LEARNING:
            run_options = [
                (CardStatus.LEARNING, td(minutes=1), self.ease),
                (CardStatus.LEARNING, td(minutes=6), self.ease, 1),
                (CardStatus.LEARNING, td(minutes=10), self.ease, 1) if self.step == 0
                else (CardStatus.REVIEWING, td(days=1), self.ease),
                (CardStatus.REVIEWING, td(days=4), self.ease, 1), # not sure why the original code do not change the step
            ]
        elif self.status == CardStatus.REVIEWING:
            run_options = [
                (CardStatus.RELEARNING, td(minutes=10), self.ease - 0.2),
                (CardStatus.REVIEWING, self.interval * 1.2, self.ease - 0.15),
                (CardStatus.REVIEWING, self.interval * self.ease, self.ease),
                (CardStatus.REVIEWING, self.interval * self.ease * 1.5, self.ease + 0.15),
            ]
        elif self.status == CardStatus.RELEARNING:
            run_options = [
                (CardStatus.RELEARNING, td(minutes=1), self.ease),
                (CardStatus.RELEARNING, td(minutes=6), self.ease),
                (CardStatus.REVIEWING, td(days=1), self.ease),
                (CardStatus.REVIEWING, td(days=4), self.ease),
            ]
        prop_to_update = run_options[level.value]
        prop_to_update = prop_to_update if len(prop_to_update) == 4 else prop_to_update + (self.step,)
        self.status, self.interval, self.ease, self.step = prop_to_update
        self.timestamp = datetime.now(timezone.utc)
