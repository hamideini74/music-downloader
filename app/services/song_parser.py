from dataclasses import dataclass


@dataclass
class SongRequest:
    artist: str
    title: str


class SongListParser:
    def parse(self, content: str) -> list[SongRequest]:
        lines = [
            line.strip()
            for line in content.splitlines()
            if line.strip()
        ]

        if not lines:
            return []

        artist = lines[0]

        return [
            SongRequest(
                artist=artist,
                title=title,
            )
            for title in lines[1:]
        ]