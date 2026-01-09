import requests
from flask import Flask, Response

app = Flask(__name__)

# L'adresse vers la source des chaînes
VAVOO_URL = "https://www2.vavoo.to/live2/index"

@app.route('/')
def get_playlist():
    try:
        # On récupère les données de Vavoo
        response = requests.get(VAVOO_URL)
        data = response.text
        
        # On renvoie le contenu en format M3U pour VLC
        return Response(data, mimetype='text/plain')
    except Exception as e:
        return f"Erreur lors de la récupération : {str(e)}", 500

if __name__ == "__main__":
    # Koyeb utilise le port 8000 par défaut
    app.run(host='0.0.0.0', port=8000)
