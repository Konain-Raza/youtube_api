from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from pytube import YouTube
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        url = query_params.get("url", [None])[0]
        download_type = query_params.get("type", ["video"])[0]  # Default is video

        if not url:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Missing 'url' parameter"}).encode("utf-8"))
            return
        
        try:
            yt = YouTube(url)
            
            if download_type == "audio":
                stream = yt.streams.filter(only_audio=True).first()
            else:
                stream = yt.streams.get_highest_resolution()

            download_url = stream.url  # Get the direct stream URL

            response = {
                "title": yt.title,
                "download_url": download_url
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
