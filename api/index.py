from fastapi import FastAPI
import yt_dlp

app = FastAPI()

@app.get("/download")
async def download(url: str):
    if not url:
        return {"error": "Missing 'url' parameter"}
    
    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'format': 'bestaudio/best+bestvideo'  # Get both audio and video
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        
        return {
            "title": info.get("title", "Unknown"),
            "thumbnail": info.get("thumbnail", ""),
            "audio_url": info.get("formats")[0]["url"],  # First format (audio)
            "video_url": info.get("url")  # Best video format
        }
    except Exception as e:
        return {"error": str(e)}

