from abc import ABC, abstractmethod


class SyncInterface(ABC):
    @abstractmethod
    def pull(self, source: str):
        pass

    @abstractmethod
    def push(self, destination: str, data, force: bool = True):
        pass
