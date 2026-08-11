from fastapi import APIRouter

from app.api.v1.endpoints import downloads
from app.api.v1.endpoints import search
from app.api.v1.endpoints import sources

router = APIRouter(prefix="/api/v1", )

router.include_router(search.router)
router.include_router(downloads.router)
router.include_router(sources.router)
