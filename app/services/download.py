from pathlib import Path

import httpx


class DownloadService:

    def __init__(self, download_dir: str = "downloads"):
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    async def download(
        self,
        url: str,
        filename: str,
    ) -> str:

        file_path = self.download_dir / filename

        async with httpx.AsyncClient(
            follow_redirects=True,
            timeout=60.0,
        ) as client:

            async with client.stream(
                "GET",
                url,
            ) as response:

                response.raise_for_status()

                with file_path.open("wb") as file:
                    async for chunk in response.aiter_bytes(
                        chunk_size=1024 * 64
                    ):
                        file.write(chunk)

        return str(file_path)