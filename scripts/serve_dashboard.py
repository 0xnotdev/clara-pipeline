"""
serve_dashboard.py — Simple HTTP server so dashboard.html can read local JSON files via fetch()
Run: python scripts/serve_dashboard.py
Then open: http://localhost:8080
"""
import http.server
import socketserver
import os

PORT = 8080

class CORSHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()
    
    def log_message(self, format, *args):
        # Only log non-asset requests
        if not any(args[0].endswith(ext) for ext in ['.css', '.js', '.ico', '.png']):
            super().log_message(format, *args)

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print(f"\n🌐 Clara Dashboard Server")
print(f"   URL: http://localhost:{PORT}/dashboard.html")
print(f"   Press Ctrl+C to stop\n")

with socketserver.TCPServer(("", PORT), CORSHandler) as httpd:
    httpd.serve_forever()
