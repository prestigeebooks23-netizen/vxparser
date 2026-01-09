import requests
from flask import Flask, Response, request, jsonify
from datetime import datetime

app = Flask(__name__)

# --- GESTION DES UTILISATEURS ET EXPIRATION ---
USER_DB = {
    "nathan": {
        "password": "2026",
        "exp_date": "2026-02-09"  # Ton lien expirera le 9 février 2026
    }
}

VAVOO_URL = "https://www2.vavoo.to/live2/index"

@app.route('/player_api.php')
def xtream_api():
    username = request.args.get('username')
    password = request.args.get('password')

    # Vérification de l'accès
    if username not in USER_DB or USER_DB[username]['password'] != password:
        return jsonify({"user_info": {"auth": 0}}), 403

    user = USER_DB[username]
    # Calcul de la date d'expiration pour l'application
    expiry_ts = int(datetime.strptime(user['exp_date'], "%Y-%m-%d").timestamp())
    
    return jsonify({
        "user_info": {
            "auth": 1,
            "status": "Active",
            "exp_date": str(expiry_ts),
            "username": username
        },
        "server_info": {"url": "votre-serveur.app", "port": "80"}
    })

@app.route('/get.php')
@app.route('/')
def get_playlist():
    # Envoie la liste des chaînes (format M3U)
    try:
        r = requests.get(VAVOO_URL)
        return Response(r.text, mimetype='text/plain')
    except:
        return "Erreur serveur", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
