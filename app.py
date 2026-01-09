import requests
from flask import Flask, Response, request, jsonify, redirect

app = Flask(__name__)

# On utilise une date extrêmement lointaine (9999) pour casser le blocage
@app.route('/player_api.php')
def xtream_api():
    return jsonify({
        "user_info": {
            "auth": 1,
            "status": "Active",
            "exp_date": "1999999999",  # Date en l'an 2033
            "username": "nathan"
        },
        "server_info": {"url": "koyeb.app", "port": "80"}
    })

@app.route('/live/<user>/<password>/<stream_id>.ts')
def stream_handler(user, password, stream_id):
    # On récupère le jeton Vavoo en direct
    try:
        res = requests.get("https://www2.vavoo.to/live2/index", timeout=5).json()
        token = next(ch['url'].split('?auth=')[1] for ch in res if '?auth=' in ch.get('url', ''))
        return redirect(f"https://vavoo.to/live2/play/{stream_id}.m3u8?auth={token}")
    except:
        return "Erreur", 500

@app.route('/')
@app.route('/get.php')
def m3u_output():
    res = requests.get("https://www2.vavoo.to/live2/index").json()
    m3u = "#EXTM3U\n"
    host = request.host_url.replace("https://", "http://").rstrip('/')
    for ch in res:
        s_id = ch['url'].split('/')[-1].split('.')[0]
        m3u += f"#EXTINF:-1 group-title=\"{ch.get('group','')}\",{ch.get('name','')}\n"
        m3u += f"{host}/live/nathan/2026/{s_id}.ts\n"
    return Response(m3u, mimetype='text/plain')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
