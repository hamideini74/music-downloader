from .base import BaseSource
from .navahang import NavahangSource


class SourceRegistry:
    def __init__(self):
        self._sources: dict[str, BaseSource] = {}

    def register(self, source: BaseSource) -> None:
        self._sources[source.name] = source

    def get(self, name: str) -> BaseSource:
        return self._sources[name]

    def all(self) -> list[BaseSource]:
        return list(self._sources.values())


source_registry = SourceRegistry()

source_registry.register(NavahangSource())
