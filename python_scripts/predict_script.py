from deezer_api import fetch_deezer_track
from knn import KnnPlaylist
from prepare_playlists import PreparePlaylists

def predict_playlist(track_name: str) -> str:
    """
    Script to predict the character playlist (Maxime, Margot, Fabien) based on the song.
    :param song_name:
    :return: Character name
    """

    df = fetch_deezer_track(track_name)
    prepare_song = PreparePlaylists()
    df = prepare_song.data_cleaning(df)

    knn_model = KnnPlaylist.load_model("knn_playlist_model.pickle")


    prediction = knn_model.predict(df)
    return prediction[0]

print(predict_playlist(""))
