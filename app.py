import requests
import re
from flask import Flask, Response, request, jsonify
from datetime import datetime

app = Flask(__name__)

USER_DB = {"nathan": {"password": "2026", "exp": "2026-12-31"}}

def force_get_token():
    """Méthode de secours pour extraire la clé de sécurité quoi qu'il arrive."""
    try:
        # On tente de récupérer la clé sur l'API directe
        headers = {'User-Agent': 'VAVOO/2.6'}
        res = requests.get("https://www2.vavoo.to/live2/index", headers=headers, timeout=10)
        content = res.text
        # Recherche par texte (plus fiable que le JSON parfois)
        match = re.search(r'\?auth=([a-zA-Z0-9._-]+)', content)
        if match:
            return match.group(1)
        return ""
    except:
        return ""

@app.route('/player_api.php')
def xtream_api():
    # Garde cette partie pour IPTV Smarters
    return jsonify({"user_info": {"auth": 1, "status": "Active", "exp_date": "1767139200", "username": "nathan"}})

@app.route('/')
@app.route('/get.php')
def final_m3u():
    token = force_get_token()
    try:
        res = requests.get("https://www2.vavoo.to/live2/index")
        channels = res.json()
        m3u = "#EXTM3U\n"
        for ch in channels:
            url = ch.get('url', '')
            if url:
                # ICI ON FORCE L'INJECTION DU TOKEN
                clean_url = url.split('?auth=')[0]
                signed_url = f"{clean_url}?auth={token}" if token else clean_url
                m3u += f"#EXTINF:-1 group-title=\"{ch.get('group','')}\",{ch.get('name','')}\n{signed_url}\n"
        return Response(m3u, mimetype='text/plain')
    except:
        return "Erreur source", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
