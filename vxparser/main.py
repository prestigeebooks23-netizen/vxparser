import os
import http.server
import socketserver
import threading
import sys

# Indique à Python où trouver tes fichiers
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

PORT = 7860

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Si l'adresse contient /vavoo, on génère la liste
        if '/vavoo' in self.path:
            try:
                self.send_response(200)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                
                import services
                # On lance la récupération des chaînes
                # Note: f=fr est géré par ton script services.py
                output = services.handler('init')
                
                self.wfile.write(str(output).encode('utf-8'))
            except Exception as e:
                self.wfile.write(f"Erreur : {str(e)}".encode())
        else:
            # Sinon on affiche les dossiers par défaut
            super().do_GET()

def run_server():
    # Permet de réutiliser le port immédiatement après un redémarrage
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"=== SERVEUR IPTV ACTIF SUR LE PORT {PORT} ===")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()







