import yt_dlp


url = "https://www.youtube.com/watch?v=IMmbi1ZsExA"

options = {
    "quiet": False,
}

with yt_dlp.YoutubeDL(options) as ydl:
    info = ydl.extract_info(url, download=False)

print("Title:", info.get("title"))
print("Uploader:", info.get("uploader"))
print("Duration:", info.get("duration"))
print("Formats:")

for fmt in info.get("formats", []):
    print(
        fmt.get("format_id"),
        fmt.get("ext"),
        fmt.get("acodec"),
        fmt.get("vcodec"),
        fmt.get("abr"),
    )