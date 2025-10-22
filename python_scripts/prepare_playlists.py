from sklearn.feature_extraction.text import TfidfVectorizer
from deezer_api import fetch_deezer_playlist



class PreparePlaylists:
    def __init__(self):
        self.playlist_tracks= list()
        self.character = list()
        self.vectorized_playlist = list()


    def __call__(self, playlist_ids: dict) -> tuple[list, list]:

        for name,id in playlist_ids.items():

            track_genras = fetch_deezer_playlist(id)
            for genras_list in track_genras:
                genras = [g.replace(" ", "_") for g in genras_list]
                self.playlist_tracks.append(" ".join(genras))

                self.character.append(name)


        return self.playlist_tracks, self.character
