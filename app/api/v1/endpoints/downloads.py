from fastapi import APIRouter, HTTPException, UploadFile, File

from app.schemas.download import (
    DownloadRequest,
    DownloadResponse,
)
from app.services.download import DownloadService
from app.services.search import SearchService
from app.services.utils import safe_filename


router = APIRouter()

download_service = DownloadService()
search_service = SearchService()


@router.post(
    "/download",
    response_model=DownloadResponse,
)
async def download(request: DownloadRequest):
    try:
        if not request.download_url:
            raise HTTPException(
                status_code=400,
                detail="Download URL is required.",
            )

        filename = safe_filename(
            artist=request.artist,
            title=request.title,
        )

        file_path = await download_service.download(
            url=str(request.download_url),
            filename=filename,
        )

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    return DownloadResponse(
        artist=request.artist,
        title=request.title,
        file_path=file_path,
    )


@router.post("/download/file")
async def download_file( file: UploadFile = File(...), ):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="File name is required.",
        )

    if not file.filename.lower().endswith(".txt"):
        raise HTTPException(
            status_code=400,
            detail="Only TXT files are supported.",
        )

    try:
        content = await file.read()
        text = content.decode("utf-8")

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        if len(lines) < 2:
            raise HTTPException(
                status_code=400,
                detail="TXT file must contain an artist and at least one song.",
            )

        artist = lines[0]
        titles = lines[1:]

        downloaded = []
        not_found = []

        for title in titles:
            results = await search_service.search(
                artist=artist,
                title=title,
            )

            if not results:
                not_found.append(title)
                continue

            result = next(
                (
                    item
                    for item in results
                    if item.download_url
                ),
                None,
            )

            if result is None:
                not_found.append(title)
                continue

            filename = safe_filename(
                artist=result.artist,
                title=result.title,
            )

            file_path = await download_service.download(
                url=result.download_url,
                filename=filename,
            )

            downloaded.append(
                {
                    "artist": result.artist,
                    "title": result.title,
                    "file_path": file_path,
                }
            )

        return {
            "artist": artist,
            "total": len(titles),
            "downloaded": len(downloaded),
            "not_found": len(not_found),
            "files": downloaded,
            "failed": not_found,
        }

    except HTTPException:
        raise

    except UnicodeDecodeError as exc:
        raise HTTPException(
            status_code=400,
            detail="TXT file must be UTF-8 encoded.",
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc