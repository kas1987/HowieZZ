#!/usr/bin/env python3
"""
Tiny local web server for the Zelex Collector's Gallery preview.

Why use this instead of just double-clicking index.html?
  Some browsers restrict things like video autoplay or file access when a
  page is opened directly from disk (the "file://" protocol). Serving the
  folder over http://localhost makes the preview behave exactly like a real
  website, so everything (looping hero video, galleries, popouts) works.

Usage:
  python serve.py            # starts server and opens your browser
    python serve.py 8000       # use a custom port instead of the default 9000

Requires: Python 3 (no extra packages). Press Ctrl+C to stop.
"""
import http.server
import socketserver
import webbrowser
import os
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 9000

# Always serve from the folder this script lives in.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

Handler = http.server.SimpleHTTPRequestHandler
# Make sure modern asset types are served with correct content types.
Handler.extensions_map.update({
    ".webp": "image/webp",
    ".mp4": "video/mp4",
    ".js": "application/javascript",
})

url = f"http://localhost:{PORT}/index.html"

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("=" * 60)
        print("  Zelex preview is running.")
        print(f"  Open this in your browser:  {url}")
        print("  (it should open automatically)")
        print("  Press Ctrl+C here to stop the server.")
        print("=" * 60)
        try:
            webbrowser.open(url)
        except Exception:
            pass
        httpd.serve_forever()
except OSError as e:
    print(f"Could not start server on port {PORT}: {e}")
    print(f"Try a different port, e.g.:  python serve.py 9000")
    sys.exit(1)
except KeyboardInterrupt:
    print("\nServer stopped. Goodbye.")
