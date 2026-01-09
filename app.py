import http.server
import socketserver
import requests

PORT = 7860

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            # Récupère les chaînes directement
            target_url = "https://www2.vavoo.to/live/index?f=fr"
            headers = {'User-Agent': 'VAVOO/2.6'}
            r = requests.get(target_url, headers=headers, timeout=10)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(r.text.encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Erreur : {str(e)}".encode())

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    httpd.serve_forever()
