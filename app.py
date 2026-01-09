import requests
from flask import Flask, Response, redirect

app = Flask(__name__)

# Source brute de Vavoo
SOURCE = "https://www2.vavoo.to/live2/index"

@app.route('/')
def get_m3u():
    try:
        # On récupère la liste des chaînes
        resp = requests.get(SOURCE, timeout=10)
        channels = resp.json()
        
        m3u = "#EXTM3U\n"
        for ch in channels:
            name = ch.get('name', 'TV')
            group = ch.get('group', 'Vavoo')
            # On utilise l'URL de redirection de notre propre serveur
            stream_url = ch.get('url', '')
            if stream_url:
                # On crée un lien qui passe par notre serveur pour être "signé"
                m3u += f'#EXTINF:-1 group-title="{group}",{name}\n'
                m3u += f'{stream_url}\n'
        
        return Response(m3u, mimetype='text/plain')
    except:
        return "Erreur de chargement", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
