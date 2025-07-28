#!/usr/bin/env python3
"""
Simple HTTP server to serve the African website
Run this script and visit http://localhost:8000/african_home.html
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(Path(__file__).parent), **kwargs)

def main():
    # Change to the templates directory
    templates_dir = Path(__file__).parent / "templates"
    
    if not templates_dir.exists():
        print("❌ Templates directory not found!")
        return
    
    # Change to templates directory
    os.chdir(templates_dir)
    
    try:
        with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
            print(f"🌍 Ubuntu Spirit - African Website Server")
            print(f"📍 Serving at http://localhost:{PORT}")
            print(f"🎯 Visit: http://localhost:{PORT}/african_home.html")
            print(f"🛑 Press Ctrl+C to stop the server")
            print("="*50)
            
            # Try to open the browser automatically
            try:
                webbrowser.open(f'http://localhost:{PORT}/african_home.html')
                print("🚀 Opening website in your default browser...")
            except:
                print("💡 Please manually open http://localhost:{PORT}/african_home.html in your browser")
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print(f"\n👋 Ubuntu Spirit server stopped. Asante sana!")
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"❌ Port {PORT} is already in use. Try a different port or stop the existing server.")
        else:
            print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    main()