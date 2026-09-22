"""Local drop box: page JS on gemini.google.com POSTs generated image bytes here (no download needed).

    .venv/bin/python tools/drop_server.py &     # listens on 127.0.0.1:5314
    POST /save?name=foo  body=image bytes  -> photos/gem/foo.png (converted to RGB PNG)
"""
import http.server, os, io
from urllib.parse import urlparse, parse_qs
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "photos", "gem"); os.makedirs(OUT, exist_ok=True)

class H(http.server.BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS, GET")
        self.send_header("Access-Control-Allow-Headers", "*")
    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()
    def do_GET(self):
        self.send_response(200); self._cors(); self.end_headers(); self.wfile.write(b"ok")
    def do_POST(self):
        q = parse_qs(urlparse(self.path).query); name = q.get("name", ["drop"])[0]
        n = int(self.headers.get("Content-Length", 0)); data = self.rfile.read(n)
        im = Image.open(io.BytesIO(data)).convert("RGB")
        p = os.path.join(OUT, name + ".png"); im.save(p)
        self.send_response(200); self._cors(); self.end_headers()
        self.wfile.write(f"{p} {im.size}".encode()); print("saved", p, im.size, flush=True)
    def log_message(self, *a): pass

http.server.ThreadingHTTPServer(("127.0.0.1", 5314), H).serve_forever()
