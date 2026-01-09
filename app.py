import requests
import re
from flask import Flask, Response, request, jsonify
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURATION DES ACCÈS ---
USER_DB = {
    "nathan": {
        "password": "2026",
        "exp_date": "2026-06-01" # Date d'expiration
    }
}

def get_vavoo_auth():
    """Récupère la clé de signature nécessaire pour lire les flux."""
    try:
        req = requests.get("https://www2.vavoo.to/live2/index", timeout=10)
        # On cherche la clé d'authentification dans l'index
        return req.text.split('?auth=')[1].split('\n')[0] if '?auth=' in req.text else ""
    except:
        return ""

@app.route('/player_api.php')
def xtream_api():
    username = request.args.get('username')
    password = request.args.get('password')
    if username not in USER_DB or USER_DB[username]['password'] != password:
        return jsonify({"user_info": {"auth": 0}}), 403
    
    user = USER_DB[username]
    expiry_ts = int(datetime.strptime(user['exp_date'], "%Y-%m-%d").timestamp())
    return jsonify({
        "user_info": {
            "auth": 1,
            "status": "Active",
            "exp_date": str(expiry_ts),
            "username": username
        },
        "server_info": {"url": "koyeb.app", "port": "80"}
    })

@app.route('/get.php')
@app.route('/')
def get_playlist():
    auth_key = get_vavoo_auth()
    try:
        r = requests.get("https://www2.vavoo.to/live2/index")
        data = r.text
        # On réécrit les liens pour qu'ils soient lisibles par VLC/IPTV Smarters
        if auth_key:
            data = data.replace('.ts', f'.ts?auth={auth_key}')
        return Response(data, mimetype='text/plain')
    except:
        return "Erreur source", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
