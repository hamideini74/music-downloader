from pydantic import BaseModel, HttpUrl


class DownloadRequest(BaseModel):
    download_url: str
    artist: str
    title: str


class DownloadResponse(BaseModel):
    artist: str
    title: str
    file_path: str