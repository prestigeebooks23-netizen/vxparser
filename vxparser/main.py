import os
import http.server
import socketserver
import sys

# On force Python à regarder dans le dossier courant
path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)

PORT = 7860

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if '/vavoo' in self.path:
            try:
                # On importe services localement pour éviter la boucle
                import services
                
                # On prépare la réponse
                self.send_response(200)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                
                # On récupère les données
                # On utilise 'init' car c'est la fonction standard de vxparser
                output = services.handler('init')
                
                self.wfile.write(str(output).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Erreur script : {str(e)}".encode())
        else:
            super().do_GET()

# Lancement propre
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serveur IPTV prêt sur le port {PORT}")
    httpd.serve_forever()








