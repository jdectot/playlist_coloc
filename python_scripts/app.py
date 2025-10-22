from flask import Flask, request, jsonify, send_from_directory

from flask_cors import CORS
import os

app = Flask(__name__, static_folder="static")
CORS(app)  # permet au front (même sur un autre domaine) d'appeler l'API

@app.route("/run", methods=["POST"])
def run():
    data = request.get_json() or {}
    song = data.get("Musique", "")
    if len(song) == 0:
        return jsonify({"error": "Musique manquante"}), 400
    elif len(song) > 50:
        return jsonify({"error": "Musique trop longue"}), 400


    return jsonify({"result": doubler(nombre)})

# Sert la page index.html (optionnel : uniquement si tu veux front sur le même service)
@app.route("/", methods=["GET"])
def index():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)