from abc import ABC, abstractmethod


class SyncInterface(ABC):
    @abstractmethod
    def pull(self, source: str):
        pass

    @abstractmethod
    def push(self, destination: str, data, force: bool = True):
        pass



























































    def get_download_link(self, blob_name: str) -> str:
        pass