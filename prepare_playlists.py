from deezer_api import fetch_deezer_playlist

class PreparePlaylists:
    def __init__(self):
        self.playlist_tracks = list()
        self.genre_to_id = dict()

    def __call__(self, playlist_id:int):

        self.playlist_tracks = fetch_deezer_playlist(playlist_id)
        self.get_genras_to_ids()
        vectorized_tracks = self.vectorize_tracks()
        print(vectorized_tracks)





    def get_genras_to_ids(self)-> dict:
        """
        Associate an id to each unique genra in the playlist tracks.
        :param key: str
        :return: dict
        """
        list_genras = []
        for track in self.playlist_tracks:
            genras = list(track.values())
            list_genras.extend((genras)[0])
        unique_genras = set(list_genras)
        print(unique_genras)

        self.genre_to_id = {item: idx for idx, item in enumerate(unique_genras)}

    def vectorize_tracks(self)-> list[tuple]:
        """
        Vectorize the playlist tracks.
        :return: list of dict
        """
        print(self.genre_to_id)
        vectorized_tracks_list = []
        for track in self.playlist_tracks:
            id = list(track.keys())[0]
            vectorized_track = [0] * (len(self.genre_to_id)+1)
            for genre in list(track.values())[0]:
                if genre in self.genre_to_id.keys():
                    genre_id = self.genre_to_id[genre]
                    vectorized_track[genre_id] = 1
                else:
                    vectorized_track[-1] = 1
            vectorized_tracks_list.append((id,vectorized_track))
        return vectorized_tracks_list





