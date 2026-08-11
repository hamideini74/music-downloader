from fastapi import APIRouter

from app.schemas.source import SourceResponse
from app.sources.registry import source_registry


router = APIRouter()


@router.get("/sources", response_model=SourceResponse)
async def get_sources():
    return {"sources": [
        source.name
        for source in source_registry.all()
    ]}