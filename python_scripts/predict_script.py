from .deezer_api import fetch_deezer_track_df, fetch_deezer_tracks_by_name
from .knn import KnnPlaylist
from .prepare_playlists import PreparePlaylists
from pathlib import Path
import pandas as pd

def get_deezer_data(track_name: str) -> list[any]:
    """
    Fetch Deezer track data and return track title and dataframe.
    :param track_name:
    :return:
    """
    list_data = fetch_deezer_tracks_by_name(track_name)
    if len(list_data) == 0:
        # return exception
        raise ValueError("Désolé, nous n'avons pas trouvé de morceau.")
    else :
        return list_data



def predict_playlist(track_id:int) -> str:
    """
    Script to predict the character playlist (Maxime, Margot, Fabien) based on the song.
    :param track_id: Deezer track ID
    :return: Character name
    """

    df = fetch_deezer_track_df(track_id)

    prepare_song = PreparePlaylists()
    df = prepare_song.data_cleaning(df)

    model_path = str(Path(__file__).parent.parent / "knn_playlist_model.pickle")

    knn_model = KnnPlaylist.load_model(model_path)

    prediction = knn_model.predict(df)
    return prediction
