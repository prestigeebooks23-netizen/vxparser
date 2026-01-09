import requests
from flask import Flask, Response, request, jsonify

app = Flask(__name__)

# Identifiants pour ton accès Xtream Codes
USER_DB = {"nathan": "2026"}

def get_live_auth():
    try:
        # On récupère le jeton de sécurité de la source
        r = requests.get("https://www2.vavoo.to/live2/index", timeout=5)
        return r.json()[0]['url'].split('auth=')[1]
    except:
        return ""

@app.route('/player_api.php')
def xtream_api():
    # Simulation d'un serveur Xtream pour IPTV Smarters
    return jsonify({
        "user_info": {"auth": 1, "status": "Active", "exp_date": "1893456000", "username": "nathan"},
        "server_info": {"url": "koyeb.app", "port": "80"}
    })

@app.route('/live/<u_name>/<p_word>/<s_id>.ts')
def stream_handler(u_name, p_word, s_id):
    if u_name != "nathan" or p_word != "2026":
        return "Auth Failed", 403
    
    auth_key = get_live_auth()
    target = f"https://vavoo.to/live2/play/{s_id}.m3u8?auth={auth_key}"
    
    # On transmet le flux en direct
    def generate():
        with requests.get(target, stream=True) as r:
            for chunk in r.iter_content(chunk_size=1024*10):
                yield chunk
    return Response(generate(), content_type='video/mp2t')

@app.route('/')
@app.route('/get.php')
def playlist_m3u():
    try:
        res = requests.get("https://www2.vavoo.to/live2/index").json()
        m3u = "#EXTM3U\n"
        host = request.host_url.rstrip('/')
        for ch in res:
            sid = ch['url'].split('/')[-1].split('.')[0]
            m3u += f"#EXTINF:-1 group-title=\"{ch.get('group','')}\",{ch.get('name','')}\n{host}/live/nathan/2026/{sid}.ts\n"
        return Response(m3u, mimetype='text/plain')
    except:
        return "Error", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
