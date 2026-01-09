import os
import http.server
import socketserver
import threading
import sys

# On s'assure que Python trouve le dossier 'vxparser'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

PORT = 7860

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Si on appelle /vavoo, on force le lancement du script de chaînes
        if self.path.startswith('/vavoo'):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            import services
            # On récupère le flux et on l'écrit directement dans la réponse
            output = services.handler('init')
            self.wfile.write(str(output).encode())
        else:
            super().do_GET()

def run_server():
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"=== SERVEUR ACTIF SUR PORT {PORT} ===")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()






