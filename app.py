import requests
import json
from flask import Flask, Response

app = Flask(__name__)

# La source brute (ce que tu vois actuellement)
VAVOO_SOURCE = "https://www2.vavoo.to/live2/index"

@app.route('/')
@app.route('/playlist.m3u')
def generate_m3u():
    try:
        # 1. On récupère le texte JSON que tu as vu
        response = requests.get(VAVOO_SOURCE)
        data = response.json() # On le transforme en liste utilisable par Python
        
        # 2. On commence à construire le fichier M3U
        m3u_content = "#EXTM3U\n"
        
        for channel in data:
            name = channel.get('name', 'Chaîne sans nom')
            group = channel.get('group', 'Vavoo')
            logo = channel.get('logo', '')
            url = channel.get('url', '')
            
            if url:
                # On ajoute chaque chaîne au bon format pour VLC/IPTV
                m3u_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n'
                m3u_content += f'{url}\n'
        
        # 3. On envoie le résultat final
        return Response(m3u_content, mimetype='text/plain')
        
    except Exception as e:
        return f"Erreur de transformation : {str(e)}", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
