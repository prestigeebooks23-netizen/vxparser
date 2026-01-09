import requests
from flask import Flask, Response, request, jsonify
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURATION XTREAM ---
USER_DB = {"nathan": {"password": "2026", "exp": "2026-12-31"}}

def get_vavoo_token():
    try:
        res = requests.get("https://www2.vavoo.to/live2/index", timeout=10)
        for ch in res.json():
            if '?auth=' in ch.get('url', ''):
                return ch['url'].split('?auth=')[1]
        return ""
    except:
        return ""

@app.route('/player_api.php')
def xtream_api():
    return jsonify({
        "user_info": {"auth": 1, "status": "Active", "exp_date": "1893456000", "username": "nathan"},
        "server_info": {"url": "koyeb.app", "port": "80"}
    })

@app.route('/live/<user>/<password>/<stream_id>.ts')
def proxy_stream(user, password, stream_id):
    # Vérification sécurité
    if user not in USER_DB or USER_DB[user]['password'] != password:
        return "Accès refusé", 403

    token = get_vavoo_token()
    target_url = f"https://vavoo.to/live2/play/{stream_id}.m3u8?auth={token}"
    
    # Mode Streaming : on transmet les données au fur et à mesure
    def generate():
        with requests.get(target_url, stream=True, headers={'User-Agent': 'VAVOO/2.6'}) as r:
            for chunk in r.iter_content(chunk_size=8192):
                yield chunk

    return Response(generate(), content_type='video/mp2t')

@app.route('/')
@app.route('/get.php')
def m3u_list():
    try:
        res = requests.get("https://www2.vavoo.to/live2/index")
        channels = res.json()
        m3u = "#EXTM3U\n"
        base = request.host_url.rstrip('/')
        for ch in channels:
            s_id = ch['url'].split('/')[-1].split('.')[0]
            # Lien formaté pour VLC et IPTV Smarters
            proxy_link = f"{base}/live/nathan/2026/{s_id}.ts"
            m3u += f"#EXTINF:-1 group-title=\"{ch.get('group','')}\",{ch.get('name','')}\n{proxy_link}\n"
        return Response(m3u, mimetype='text/plain')
    except:
        return "Erreur", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
