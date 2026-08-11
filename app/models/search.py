from dataclasses import dataclass


@dataclass
class SearchResult:
    artist: str
    title: str
    url: str
    source: str
    download_url: str | None = None
