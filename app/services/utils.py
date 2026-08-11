import re


def safe_filename(artist: str, title: str) -> str:
    filename = f"{artist} - {title}"

    filename = re.sub(
        r'[<>:"/\\|?*]',
        "_",
        filename,
    )

    return f"{filename}.mp3"