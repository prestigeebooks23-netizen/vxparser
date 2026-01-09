import requests
from flask import Flask, Response

app = Flask(__name__)

def get_vavoo_token():
    """Récupère la clé de sécurité nécessaire pour lire les flux."""
    try:
        # On interroge l'index pour obtenir le jeton 'auth'
        res = requests.get("https://www2.vavoo.to/live2/index", timeout=10)
        data = res.json()
        # On cherche un lien pour extraire la clé auth
        first_url = data[0].get('url', '')
        if '?auth=' in first_url:
            return first_url.split('?auth=')[1]
        return ""
    except:
        return ""

@app.route('/')
@app.route('/playlist.m3u')
def generate_m3u():
    try:
        token = get_vavoo_token()
        response = requests.get("https://www2.vavoo.to/live2/index")
        channels = response.json()
        
        m3u_content = "#EXTM3U\n"
        for ch in channels:
            name = ch.get('name', 'TV')
            group = ch.get('group', 'Vavoo')
            logo = ch.get('logo', '')
            url = ch.get('url', '')
            
            if url:
                # On ajoute la clé de sécurité à la fin de chaque lien
                final_url = f"{url}?auth={token}" if token else url
                m3u_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n'
                m3u_content += f'{final_url}\n'
        
        return Response(m3u_content, mimetype='text/plain')
    except Exception as e:
        return f"Erreur : {str(e)}", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
