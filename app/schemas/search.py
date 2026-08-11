from pydantic import BaseModel


class SearchRequest(BaseModel):
    artist: str
    title: str

class SearchResultResponse(BaseModel):
    artist: str
    title: str
    url: str
    source: str
    download_url: str | None = None

class SearchResponse(BaseModel):
    artist: str
    title: str
    results: list[SearchResultResponse]