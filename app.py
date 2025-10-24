from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from python_scripts.predict_script import predict_playlist, get_deezer_data

app = Flask(__name__, static_folder="static")
CORS(app)  # permet au front (même sur un autre domaine) d'appeler l'API
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search_song", methods=["POST"])
def search_song():
    data = request.get_json() or {}
    track_name = data.get("Musique", "")
    if len(track_name) == 0:
        return jsonify({"error": "Musique manquante"}), 400
    elif len(track_name) > 100:
        return jsonify({"error": "Musique trop longue"}), 400


    return jsonify({"result": get_deezer_data(track_name)})



@app.route("/predict_song", methods=["POST"])
def predict_song():
    data = request.get_json() or {}
    track_id = data.get("id")

    return jsonify({"result": predict_playlist(track_id)})


# Sert la page index.html (optionnel : uniquement si tu veux front sur le même service)
@app.route("/", methods=["GET"])
def index():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)