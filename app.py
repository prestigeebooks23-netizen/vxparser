import requests
from flask import Flask, Response, request, jsonify

app = Flask(__name__)

# Infos de connexion pour ton Xtream Code
USER_DB = {"nathan": "2026"}

def get_token():
    try:
        r = requests.get("https://www2.vavoo.to/live2/index", timeout=5)
        return r.json()[0]['url'].split('auth=')[1]
    except:
        return ""

@app.route('/player_api.php')
def api():
    # Simulation parfaite de l'interface Xtream Codes
    return jsonify({
        "user_info": {"auth": 1, "status": "Active", "exp_date": "1893456000", "username": "nathan"},
        "server_info": {"url": "koyeb.app", "port": "80"}
    })

@app.route('/live/<u riots>/<p>/<id>.ts')
def stream(u, p, id):
    if u != "nathan" or p != "2026":
        return "Unauthorized", 403
    
    auth = get_token()
    # Lien direct vers le flux original pour plus de rapidité
    url = f"https://vavoo.to/live2/play/{id}.m3u8?auth={auth}"
    return Response(requests.get(url, stream=True).iter_content(chunk_size=1024*10), content_type='video/mp2t')

@app.route('/')
@app.route('/get.php')
def m3u():
    try:
        data = requests.get("https://www2.vavoo.to/live2/index").json()
        m3u = "#EXTM3U\n"
        host = request.host_url.rstrip('/')
        for ch in data:
            s_id = ch['url'].split('/')[-1].split('.')[0]
            m3u += f"#EXTINF:-1 group-title=\"{ch.get('group','')}\",{ch.get('name','')}\n{host}/live/nathan/2026/{s_id}.ts\n"
        return Response(m3u, mimetype='text/plain')
    except:
        return "Error", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
