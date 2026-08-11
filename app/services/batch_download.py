from app.services.download import DownloadService
from app.services.filename import safe_filename


class BatchDownloadService:

    def __init__(self):
        self.download_service = DownloadService()

    async def download_all(self, songs):
        results = []

        for song in songs:

            successful = False
            file_path = None
            error = None

            for search_result in song["search_results"]:

                if not search_result.download_url:
                    continue

                try:
                    filename = safe_filename(
                        artist=search_result.artist,
                        title=search_result.title,
                    )

                    file_path = (
                        await self.download_service.download(
                            url=search_result.download_url,
                            filename=filename,
                        )
                    )

                    successful = True
                    break

                except Exception as exc:
                    error = str(exc)

            results.append(
                {
                    "artist": song["artist"],
                    "title": song["title"],
                    "success": successful,
                    "file_path": file_path,
                    "error": error,
                }
            )

        return results