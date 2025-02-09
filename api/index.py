import yt_dlp
import json

def handler(request, response):
    video_url = request.args.get("url")

    if not video_url:
        response.status_code = 400
        return response.json({"error": "Missing 'url' parameter"})

    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'format': 'bestaudio/best'  # Best quality available
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

        return response.json({
            "title": info.get("title", "Unknown"),
            "thumbnail": info.get("thumbnail", ""),
            "download_url": info.get("url")
        })

    except Exception as e:
        response.status_code = 500
        return response.json({"error": str(e)})
