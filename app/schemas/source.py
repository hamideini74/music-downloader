from pydantic import BaseModel

class SourceResponse(BaseModel):
    sources: list[str]