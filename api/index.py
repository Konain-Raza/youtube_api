from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/download", methods=["GET"])
def handler():
    video_url = request.args.get("url")

    if not video_url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'format': 'bestaudio/best+bestvideo/best'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

        audio_url = None
        video_url = None

        formats = info.get("formats", [])
        for f in formats:
            if f.get("acodec") != "none" and f.get("vcodec") == "none":  # Audio-only
                audio_url = f.get("url")
            if f.get("vcodec") != "none" and f.get("acodec") == "none":  # Video-only
                video_url = f.get("url")

        return jsonify({
            "title": info.get("title", "Unknown"),
            "thumbnail": info.get("thumbnail", ""),
            "video_url": video_url,
            "audio_url": audio_url
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ REMOVE app.run() since Vercel auto-handles it
