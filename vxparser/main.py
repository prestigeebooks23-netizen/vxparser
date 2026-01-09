import os
import http.server
import socketserver
import requests

PORT = 7860

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if '/vavoo' in self.path:
            try:
                # On va chercher la liste directement à la source Vavoo
                # au lieu de passer par les fichiers qui plantent
                url = "https://www2.vavoo.to/live/index"
                headers = {'User-Agent': 'VAVOO/2.6'}
                response = requests.get(url, headers=headers, params={'f': 'fr'})
                
                self.send_response(200)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                
                # On renvoie le résultat propre
                self.wfile.write(response.text.encode('utf-8'))
            except Exception as e:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(f"Erreur de connexion : {str(e)}".encode())
        else:
            super().do_GET()

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serveur d'urgence actif")
    httpd.serve_forever()










