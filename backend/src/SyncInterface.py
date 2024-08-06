from abc import ABC, abstractmethod
from typing import List
from Card import Card

class SyncInterface(ABC):
    @abstractmethod
    def Pull(self, source: str):
        pass

    @abstractmethod
    def Push(self, destination: str, data, force: bool = True):
        pass