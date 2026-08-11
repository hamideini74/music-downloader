from abc import ABC, abstractmethod

from app.models.search import SearchResult


class BaseSource(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    async def search(self, artist: str, title: str, ) -> list[SearchResult]:
        pass
