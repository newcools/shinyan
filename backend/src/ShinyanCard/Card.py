from datetime import timezone, datetime, timedelta as td
from CardStatus import CardStatus
from CardMasterLevel import CardMasterLevel
import uuid

class Card:
    def __init__(self, name, key = None, status : CardStatus = CardStatus.LEARNING, interval=None, ease : float=2.5, step=0, timestamp=None):
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

    def __repr__(self):
        return f"Card(status={self.status}, step={self.step}, interval={self.interval}, ease={self.ease}, timestamp={self.timestamp})"
    
    def options(self):
        if self.status == CardStatus.LEARNING:
            options = [
                Card(self._name, self.key, CardStatus.LEARNING, td(minutes=1)),
                Card(self._name, self.key, CardStatus.LEARNING, td(minutes=6), step=1),
                Card(self._name, self.key, CardStatus.LEARNING, td(minutes=10), step=1) if self.step == 0 else Card(CardStatus.REVIEWING, td(days=1)),
                Card(self._name, self.key, CardStatus.REVIEWING, td(days=4)),
            ]
        elif self.status == CardStatus.REVIEWING:
            options = [
                Card(self._name, self.key, CardStatus.RELEARNING, td(minutes=10), self.ease - 0.2),
                Card(self._name, self.key, CardStatus.REVIEWING, self.interval * 1.2, self.ease - 0.15),
                Card(self._name, self.key, CardStatus.REVIEWING, self.interval * self.ease, self.ease),
                Card(self._name, self.key, CardStatus.REVIEWING, self.interval * self.ease * 1.5, self.ease + 0.15),
            ]
        elif self.status == CardStatus.RELEARNING:
            options = [
                Card(self._name, self.key, CardStatus.RELEARNING, td(minutes=1), self.ease),
                Card(self._name, self.key, CardStatus.RELEARNING, td(minutes=6), self.ease),
                Card(self._name, self.key, CardStatus.REVIEWING, td(days=1), self.ease),
                Card(self._name, self.key, CardStatus.REVIEWING, td(days=4), self.ease),
            ]
        return list(zip([CardMasterLevel.AGAIN, CardMasterLevel.HARD, CardMasterLevel.GOOD, CardMasterLevel.EASY], options))