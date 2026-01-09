import os
from http.server import SimpleHTTPRequestHandler
import socketserver
import threading

# Hugging Face utilise toujours le port 7860
PORT = 7860

def run_vavoo():
    print("=== LANCEMENT VAVOO ===")
    import services
    services.handler('init')

# Lancement du serveur web pour Hugging Face
handler = SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), handler)

print(f"=== SERVEUR ACTIF SUR PORT {PORT} ===")
# Lancer Vavoo dans un fil séparé
threading.Thread(target=run_vavoo).start()

# Garder le serveur web actif
httpd.serve_forever()





