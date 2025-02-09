import yt_dlp
import json

def handler(request):
    query = request.args
    video_url = query.get("url")

    if not video_url:
        return {"error": "Missing 'url' parameter"}, 400

    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'format': 'bestaudio/best'  # Best audio & video
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

            return {
                "title": info.get("title", "Unknown"),
                "thumbnail": info.get("thumbnail", ""),
                "download_url": info.get("url")
            }, 200

    except Exception as e:
        return {"error": str(e)}, 500
