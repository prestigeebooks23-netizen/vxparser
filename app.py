# --- CONFIGURATION UTILISATEUR ---
# On met une date en 2030 pour être tranquille
USER_DB = {
    "nathan": {"password": "2026", "exp_date": "2030-12-31", "timestamp": 1924898400}
}

@app.route('/player_api.php')
def xtream_api():
    username = request.args.get('username')
    password = request.args.get('password')
    
    # Vérification des identifiants
    if username not in USER_DB or USER_DB[username]['password'] != password:
        return jsonify({"user_info": {"auth": 0}}), 403
    
    user = USER_DB[username]
    return jsonify({
        "user_info": {
            "auth": 1,
            "status": "Active",
            "exp_date": str(user['timestamp']), # Date au format timestamp pour les lecteurs
            "is_trial": "0",
            "active_cons": "0",
            "max_connections": "1",
            "username": username
        },
        "server_info": {
            "url": "koyeb.app",
            "port": "80",
            "server_protocol": "http",
            "timezone": "Europe/Paris"
        }
    })
