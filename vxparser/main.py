import os
import http.server
import socketserver
import sys

# Simulation des attributs manquants pour éviter l'erreur circular import
class MockJobs:
    def __init__(self): self.running = False
import types
mock_module = types.ModuleType('jobs')
mock_module.jobs = MockJobs()
sys.modules['jobs'] = mock_module

# Ajout du chemin des fichiers
path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)

PORT = 7860

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if '/vavoo' in self.path:
            try:
                # Importation forcée
                import services
                # On essaie de récupérer la liste des chaînes
                output = services.handler('init')
                
                self.send_response(200)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(str(output).encode('utf-8'))
            except Exception as e:
                self.send_response(200) # On envoie quand même 200 pour voir l'erreur
                self.end_headers()
                self.wfile.write(f"Diagnostic : {str(e)}".encode())
        else:
            super().do_GET()

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serveur actif")
    httpd.serve_forever()









