import requests
from flask import Flask, Response, request, jsonify
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURATION XTREAM ---
USER_DB = {
    "nathan": {"password": "2026", "exp": "2026-12-31"}
}

def get_vavoo_data():
    """Récupère les chaînes et la clé auth en une seule fois."""
    try:
        res = requests.get("https://www2.vavoo.to/live2/index", timeout=10)
        data = res.json()
        # On extrait la clé auth du premier lien trouvé
        auth_token = ""
        for ch in data:
            if '?auth=' in ch.get('url', ''):
                auth_token = ch['url'].split('?auth=')[1]
                break
        return data, auth_token
    except:
        return [], ""

@app.route('/player_api.php')
def xtream_api():
    username = request.args.get('username')
    password = request.args.get('password')
    if username not in USER_DB or USER_DB[username]['password'] != password:
        return jsonify({"user_info": {"auth": 0}}), 403
    
    exp_ts = int(datetime.strptime(USER_DB[username]['exp'], "%Y-%m-%d").timestamp())
    return jsonify({
        "user_info": {"auth": 1, "status": "Active", "exp_date": str(exp_ts), "username": username},
        "server_info": {"url": "koyeb.app", "port": "80"}
    })

@app.route('/')
@app.route('/get.php')
def generate_m3u():
    channels, token = get_vavoo_data()
    m3u = "#EXTM3U\n"
    for ch in channels:
        name = ch.get('name', 'TV')
        group = ch.get('group', 'Vavoo')
        logo = ch.get('logo', '')
        url = ch.get('url', '')
        if url:
            # On ajoute la clé auth pour que le flux s'ouvre !
            final_url = f"{url}?auth={token}" if token and '?auth=' not in url else url
            m3u += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n{final_url}\n'
    return Response(m3u, mimetype='text/plain')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
