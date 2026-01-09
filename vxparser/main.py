import os
import http.server
import socketserver
import requests

# Hugging Face utilise obligatoirement le port 7860
PORT = 7860

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Cette condition accepte n'importe quelle demande contenant 'vavoo'
        if 'vavoo' in self.path:
            try:
                # On va chercher la liste directement chez Vavoo
                target_url = "https://www2.vavoo.to/live/index?f=fr"
                headers = {'User-Agent': 'VAVOO/2.6'}
                r = requests.get(target_url, headers=headers, timeout=10)
                
                # On renvoie le résultat au navigateur
                self.send_response(200)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(r.text.encode('utf-8'))
            except Exception as e:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(f"Erreur de connexion : {str(e)}".encode())
        else:
            # Si on tape juste l'adresse de base, on affiche un message d'aide
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Serveur actif. Utilisez : /vavoo?f=fr")

# Configuration du serveur
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serveur IPTV de secours actif sur le port {PORT}")
    httpd.serve_forever()










