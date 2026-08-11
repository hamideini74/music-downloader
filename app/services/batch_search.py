from app.services.search import SearchService
from app.services.song_parser import SongRequest
from app.services.song_normalizer import SongNormalizer


class BatchSearchService:

    def __init__(self):
        self.search_service = SearchService()
        self.normalizer = SongNormalizer()

    async def search(self, songs: list[SongRequest]):
        results = []

        for song in songs:
            artist = self.normalizer.normalize_artist(
                song.artist
            )
            title = self.normalizer.normalize_title(
                song.title
            )

            search_results = await self.search_service.search(
                artist=artist,
                title=title,
            )

            results.append(
                {
                    "artist": song.artist,
                    "title": song.title,
                    "search_results": search_results,
                }
            )

        return results