import requests
from flask import Flask, Response, request, jsonify, redirect

app = Flask(__name__)

# --- CONFIGURATION PROFESSIONNELLE ---
# Ton accès pour IPTV Smarters
USER_DB = {"nathan": {"password": "2026", "exp": "2026-12-31"}}

def get_fresh_auth():
    """La Clé : va chercher le jeton de déblocage chez Vavoo."""
    try:
        res = requests.get("https://www2.vavoo.to/live2/index", timeout=10)
        data = res.json()
        for ch in data:
            if '?auth=' in ch.get('url', ''):
                return ch['url'].split('?auth=')[1]
        return ""
    except:
        return ""

@app.route('/player_api.php')
def xtream_api():
    """API Xtream pour connecter IPTV Smarters."""
    return jsonify({
        "user_info": {"auth": 1, "status": "Active", "exp_date": "1767139200", "username": "nathan"},
        "server_info": {"url": "koyeb.app", "port": "80"}
    })

@app.route('/live/<user>/<password>/<stream_id>.ts')
def stream_handler(user, password, stream_id):
    """C'est ici que le déblocage se fait pour VLC et Smarters."""
    if user not in USER_DB or USER_DB[user]['password'] != password:
        return "Accès Refusé", 403

    # On récupère la signature juste avant de lancer la vidéo
    token = get_fresh_auth()
    # On construit l'URL de déblocage
    target_url = f"https://vavoo.to/live2/play/{stream_id}.m3u8?auth={token}"
    
    # REDIRECTION : On envoie le flux débloqué directement au lecteur
    return redirect(target_url)

@app.route('/')
@app.route('/get.php')
def m3u_output():
    """Génère la liste parfaite que tu as vue à 18h11."""
    try:
        res = requests.get("https://www2.vavoo.to/live2/index")
        channels = res.json()
        m3u = "#EXTM3U\n"
        # On force le HTTP pour éviter les erreurs de certificat sur VLC
        base = request.host_url.replace("https://", "http://").rstrip('/')
        for ch in channels:
            s_id = ch['url'].split('/')[-1].split('.')[0]
            m3u += f"#EXTINF:-1 group-title=\"{ch.get('group','')}\",{ch.get('name','')}\n"
            m3u += f"{base}/live/nathan/2026/{s_id}.ts\n"
        return Response(m3u, mimetype='text/plain')
    except:
        return "Erreur Serveur", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
