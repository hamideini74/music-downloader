from urllib.parse import quote_plus, urljoin

import httpx
from bs4 import BeautifulSoup

from app.models.search import SearchResult
from .base import BaseSource


class NavahangSource(BaseSource):
    BASE_URL = "https://www.navahang.com"

    @property
    def name(self) -> str:
        return "navahang"

    async def search(self, artist: str, title: str) -> list[SearchResult]:
        query = f"{artist} {title}"

        search_url = (
            f"{self.BASE_URL}/main-search.php"
            f"?q={quote_plus(query)}&size=50&suggestion=true"
        )

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/151.0.0.0 Safari/537.36"
            ),
            "Accept": "application/json",
        }

        async with httpx.AsyncClient(
            headers=headers,
            follow_redirects=True,
            timeout=10.0,
        ) as client:

            response = await client.get(search_url)
            response.raise_for_status()

            data = response.json()

            results = []

            for item in data.get("MP3", []):
                song_url = urljoin(
                    self.BASE_URL,
                    item["url"],
                )

                song_response = await client.get(song_url)
                song_response.raise_for_status()

                soup = BeautifulSoup(
                    song_response.text,
                    "html.parser",
                )

                audio_meta = soup.find(
                    "meta",
                    property="og:audio",
                )

                download_url = None

                if audio_meta:
                    download_url = audio_meta.get("content")

                results.append(
                    SearchResult(
                        artist=item.get("artist_name", ""),
                        title=item.get("song_name", ""),
                        url=song_url,
                        source=self.name,
                        download_url=download_url,
                    )
                )

        return results