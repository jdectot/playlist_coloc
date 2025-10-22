from deezer_api import fetch_deezer_track
from knn import KnnPlaylist
from prepare_playlists import PreparePlaylists

def predict_playlist(track_name: str) -> str:
    """
    Script to predict the character playlist (Maxime, Margot, Fabien) based on the song.
    :param song_name:
    :return: Character name
    """

    track_genras = fetch_deezer_track(track_name)
    genras = [g.replace(" ", "_") for g in track_genras]
    genras = [" ".join(genras)]

    knn_model = KnnPlaylist.load_model("knn_playlist_model.pickle")


    prediction = knn_model.predict(genras)
    return prediction[0]

print(predict_playlist("Dancing Queen"))
