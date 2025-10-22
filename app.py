from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from python_scripts.predict_script import predict_playlist
import os

app = Flask(__name__, static_folder="static")
CORS(app)  # permet au front (même sur un autre domaine) d'appeler l'API
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run():
    data = request.get_json() or {}
    song_name = data.get("Musique", "Blinding Lights")
    if len(song_name) == 0:
        return jsonify({"error": "Musique manquante"}), 400
    elif len(song_name) > 100:
        return jsonify({"error": "Musique trop longue"}), 400


    return jsonify({"result": predict_playlist(song_name)})

# Sert la page index.html (optionnel : uniquement si tu veux front sur le même service)
@app.route("/", methods=["GET"])
def index():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)