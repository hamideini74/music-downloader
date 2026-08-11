from fastapi import APIRouter

from app.schemas.search import SearchRequest, SearchResponse, SearchResultResponse
from app.services.search import SearchService

router = APIRouter()
search_service = SearchService()

@router.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    results = await search_service.search(
        artist=request.artist,
        title=request.title,
    )

    return SearchResponse(
        artist=request.artist,
        title=request.title,
        results=[
            SearchResultResponse(
                artist=result.artist,
                title=result.title,
                url=result.url,
                download_url=result.download_url,
                source=result.source,
            )
            for result in results
        ],
    )