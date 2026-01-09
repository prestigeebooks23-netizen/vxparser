import requests
import re
from flask import Flask, Response, request, jsonify

app = Flask(__name__)

# Utilise un User-Agent de télévision pour ne pas être bloqué
HEADERS = {
    'User-Agent': 'VAVOO/2.6',
    'Accept': '*/*',
    'Connection': 'keep-alive'
}

def get_vavoo_token():
    """Récupère la clé de sécurité par une méthode directe."""
    try:
        # On interroge l'API de signature de Vavoo
        response = requests.get("https://www2.vavoo.to/live2/index", headers=HEADERS, timeout=15)
        text = response.text
        # On cherche le jeton dans le texte brut
        token_match = re.search(r'\?auth=([a-zA-Z0-9._-]+)', text)
        if token_match:
            return token_match.group(1)
        
        # Deuxième tentative si le premier échec
        data = response.json()
        for item in data:
            if '?auth=' in item.get('url', ''):
                return item['url'].split('?auth=')[1]
        return ""
    except:
        return ""

@app.route('/player_api.php')
def xtream_api():
    """Simule l'API Xtream pour IPTV Smarters."""
    return jsonify({
        "user_info": {"auth": 1, "status": "Active", "exp_date": "1893456000", "username": "nathan"},
        "server_info": {"url": "koyeb.app", "port": "80"}
    })

@app.route('/')
@app.route('/get.php')
def serve_playlist():
    token = get_vavoo_token()
    try:
        res = requests.get("https://www2.vavoo.to/live2/index", headers=HEADERS)
        channels = res.json()
        
        output = "#EXTM3U\n"
        for ch in channels:
            name = ch.get('name', 'TV')
            url = ch.get('url', '').split('?auth=')[0] # On nettoie l'URL
            if url:
                # ON FORCE L'INJECTION DU TOKEN ICI
                final_url = f"{url}?auth={token}" if token else url
                output += f"#EXTINF:-1 group-title=\"{ch.get('group', 'Vavoo')}\",{name}\n{final_url}\n"
        
        return Response(output, mimetype='text/plain')
    except Exception as e:
        return f"Erreur : {str(e)}", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
