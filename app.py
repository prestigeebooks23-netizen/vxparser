import requests
from flask import Flask, Response, request, jsonify, redirect

# Ligne cruciale pour corriger l'erreur de 19:02
app = Flask(__name__)

# CONFIGURATION : Date en 2030 pour corriger l'erreur "Expired"
USER_DB = {
    "nathan": {"password": "2026", "timestamp": 1924898400}
}

def get_fresh_auth():
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
    username = request.args.get('username')
    password = request.args.get('password')
    
    if username not in USER_DB or USER_DB[username]['password'] != password:
        return jsonify({"user_info": {"auth": 0}}), 403
    
    return jsonify({
        "user_info": {
            "auth": 1,
            "status": "Active",
            "exp_date": "1924898400", # Décembre 2030
            "username": username
        },
        "server_info": {"url": "koyeb.app", "port": "80"}
    })

@app.route('/live/<user>/<password>/<stream_id>.ts')
def stream_handler(user, password, stream_id):
    if user not in USER_DB or USER_DB[user]['password'] != password:
        return "Accès Refusé", 403
    token = get_fresh_auth()
    return redirect(f"https://vavoo.to/live2/play/{stream_id}.m3u8?auth={token}")

@app.route('/')
@app.route('/get.php')
def m3u_output():
    try:
        res = requests.get("https://www2.vavoo.to/live2/index")
        channels = res.json()
        m3u = "#EXTM3U\n"
        host = request.host_url.replace("https://", "http://").rstrip('/')
        for ch in channels:
            s_id = ch['url'].split('/')[-1].split('.')[0]
            m3u += f"#EXTINF:-1 group-title=\"{ch.get('group','')}\",{ch.get('name','')}\n"
            m3u += f"{host}/live/nathan/2026/{s_id}.ts\n"
        return Response(m3u, mimetype='text/plain')
    except:
        return "Erreur", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
