import requests
from flask import Flask, Response, request, jsonify
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURATION XTREAM ---
# Tu peux changer l'utilisateur 'nathan' et le mot de passe '2026' ici.
USER_DB = {
    "nathan": {"password": "2026", "exp": "2026-12-31"}
}

def get_vavoo_data():
    """Récupère les chaînes et injecte la clé auth de sécurité."""
    try:
        # On récupère l'index brut de Vavoo
        res = requests.get("https://www2.vavoo.to/live2/index", timeout=10)
        data = res.json()
        
        # On va chercher la clé 'auth' qui change régulièrement
        auth_token = ""
        # On essaie de la trouver sur la première chaîne de la liste
        for ch in data:
            raw_url = ch.get('url', '')
            if '?auth=' in raw_url:
                auth_token = raw_url.split('?auth=')[1]
                break
        
        return data, auth_token
    except:
        return [], ""

@app.route('/player_api.php')
def xtream_api():
    """Interface pour IPTV Smarters et TiviMate."""
    username = request.args.get('username')
    password = request.args.get('password')
    
    if username not in USER_DB or USER_DB[username]['password'] != password:
        return jsonify({"user_info": {"auth": 0}}), 403
    
    exp_ts = int(datetime.strptime(USER_DB[username]['exp'], "%Y-%m-%d").timestamp())
    return jsonify({
        "user_info": {
            "auth": 1,
            "status": "Active",
            "exp_date": str(exp_ts),
            "username": username
        },
        "server_info": {"url": "koyeb.app", "port": "80"}
    })

@app.route('/')
@app.route('/get.php')
def generate_playlist():
    """Génère la playlist M3U fonctionnelle avec les clés de sécurité."""
    channels, token = get_vavoo_data()
    m3u = "#EXTM3U\n"
    
    for ch in channels:
        name = ch.get('name', 'TV')
        group = ch.get('group', 'Vavoo')
        logo = ch.get('logo', '')
        url = ch.get('url', '')
        
        if url:
            # On s'assure que chaque lien a bien la clé auth à la fin
            # Si le lien n'a pas déjà de auth, on l'ajoute
            clean_url = url.split('?auth=')[0]
            final_url = f"{clean_url}?auth={token}" if token else clean_url
            
            m3u += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n{final_url}\n'
            
    return Response(m3u, mimetype='text/plain')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
