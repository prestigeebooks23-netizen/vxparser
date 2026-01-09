import requests
from flask import Flask, Response, request, jsonify
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURATION ---
USER_DB = {
    "nathan": {
        "password": "2026",
        "exp_date": "2026-02-09"  # Format: AAAA-MM-JJ (Exire dans 1 mois)
    }
}
VAVOO_URL = "https://www2.vavoo.to/live2/index"

@app.route('/player_api.php')
def xtream_api():
    username = request.args.get('username')
    password = request.args.get('password')

    # Vérification utilisateur
    if username not in USER_DB or USER_DB[username]['password'] != password:
        return jsonify({"user_info": {"auth": 0}}), 403

    user = USER_DB[username]
    # Vérification date
    expiry_ts = int(datetime.strptime(user['exp_date'], "%Y-%m-%d").timestamp())
    
    # Si l'app demande juste les infos
    action = request.args.get('action')
    if not action:
        return jsonify({
            "user_info": {
                "auth": 1,
                "status": "Active",
                "exp_date": str(expiry_ts),
                "username": username
            },
            "server_info": {"url": "votre-serveur.app", "port": "80"}
        })
    
    return jsonify([]) # Pour IPTV Smarters

@app.route('/get.php')
@app.route('/')
def get_m3u():
    # On récupère le flux Vavoo et on le sert
    try:
        r = requests.get(VAVOO_URL)
        return Response(r.text, mimetype='text/plain')
    except:
        return "Erreur", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
