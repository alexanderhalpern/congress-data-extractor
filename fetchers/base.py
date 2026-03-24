from abc import ABC, abstractmethod


class BaseFetcher(ABC):
    @abstractmethod
    def can_handle(self, url: str) -> bool:
        pass

    @abstractmethod
    def fetch(self, url: str) -> str | None:
        pass
