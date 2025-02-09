import yt_dlp
from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            from urllib.parse import urlparse, parse_qs
            query_components = parse_qs(urlparse(self.path).query)
            url = query_components.get("url", [None])[0]
            media_type = query_components.get("type", ["video"])[0]

            if not url:
                self.send_error(400, "Missing YouTube URL")
                return

            ydl_opts = {
                'format': 'bestaudio/best' if media_type == "audio" else 'bestvideo+bestaudio/best',
                'quiet': True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                download_url = info["url"]

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"download_url": download_url}).encode("utf-8"))
        
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
