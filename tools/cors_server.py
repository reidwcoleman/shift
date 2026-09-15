"""Serve repo files to the browser with CORS (so page JS on gemini.google.com can fetch mockups)."""
import http.server, sys, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
class H(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*"); super().end_headers()
    def log_message(self, *a): pass
http.server.ThreadingHTTPServer(("127.0.0.1", 5313), H).serve_forever()
