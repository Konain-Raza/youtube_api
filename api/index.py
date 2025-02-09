from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/download", methods=["GET"])
def handler():
    video_url = request.args.get("url")
    print("Starting API...")

    if not video_url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'format': 'bestaudio/best'  # Best quality available
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

        return jsonify({
            "title": info.get("title", "Unknown"),
            "thumbnail": info.get("thumbnail", ""),
            "download_url": info.get("url")
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Running Flask app on port 8000...")
    app.run(debug=True, host="0.0.0.0", port=8000)
