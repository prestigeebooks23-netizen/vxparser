import requests
from flask import Flask, Response, request, jsonify

app = Flask(__name__)

# --- CONFIGURATION XTREAM ---
# Identifiants pour IPTV Smarters
USER_DATA = {"nathan": "2026"}

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
    # Simule un serveur Xtream Codes professionnel
    return jsonify({
        "user_info": {"auth": 1, "status": "Active", "exp_date": "1893456000", "username": "nathan"},
        "server_info": {"url": "koyeb.app", "port": "80"}
    })

@app.route('/live/<user>/<password>/<stream_id>.ts')
@app.route('/play/<stream_id>')
def proxy_stream(stream_id, user=None, password=None):
    # Ce tunnel permet de contourner les blocages IP
    token = get_vavoo_token()
    target_url = f"https://vavoo.to/live2/play/{stream_id}.m3u8?auth={token}"
    
    # On demande au serveur Koyeb de lire le flux pour nous
    req = requests.get(target_url, stream=True, headers={'User-Agent': 'VAVOO/2.6'})
    return Response(req.iter_content(chunk_size=1024), content_type=req.headers['Content-Type'])

@app.route('/')
@app.route('/get.php')
def m3u_list():
    try:
        res = requests.get("https://www2.vavoo.to/live2/index")
        channels = res.json()
        m3u = "#EXTM3U\n"
        base_url = request.host_url.rstrip('/')
        for ch in channels:
            # On transforme chaque lien pour qu'il passe par TON tunnel
            s_id = ch['url'].split('/')[-1].split('.')[0]
            proxy_link = f"{base_url}/live/nathan/2026/{s_id}.ts"
            m3u += f"#EXTINF:-1 group-title=\"{ch.get('group','')}\",{ch.get('name','')}\n{proxy_link}\n"
        return Response(m3u, mimetype='text/plain')
    except:
        return "Erreur", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
