from app.sources.registry import source_registry


class SearchService:

    async def search(self, artist: str, title: str):
        results = []

        for source in source_registry.all():
            source_results = await source.search(
                artist=artist,
                title=title,
            )

            results.extend(source_results)

        return results
