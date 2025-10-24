import time
import deezer
import pandas as pd

def fetch_deezer_playlist(playlist_id: int, playlist_name: str)-> list[list[str]]:
    """
    Fetch Deezer playlist tracks and their details.
    :param playlist_id:
    :return:[{track_id: [genra1, genra2,...]},...]
    """

    client = deezer.Client()
    tracks_df = pd.DataFrame(columns=["track_id", "playlist_name", "artist", "album", "release_year", "genras","related_artists"])

    try:
        playlists = client.get_playlist(playlist_id)
    except Exception as e:
        print(f"Error fetching playlist {playlist_id}: {e}")
        return tracks_df

    for track in playlists.tracks:
        try :
            track_album = track.get_album()
            track_artist = track.get_artist()
            similar_artists = track_artist.get_related()
            genras = track_album.genres
            genras_name = [genre.name for genre in genras]
            tracks_df = pd.concat([tracks_df, pd.DataFrame([{
                "track_id": track.id,
                "playlist_name": playlist_name,
                "artist": track_artist.name,
                "album": track_album.title,
                "release_year": track_album.release_date,
                "genras": genras_name,
                "related_artists": [artist.name for artist in similar_artists]
            }])], ignore_index=True)

        except :
            time.sleep(3)
            try :
                track_album = track.get_album()
                track_artist = track.get_artist()
                similar_artists = track_artist.get_related()
                genras = track_album.genres
                genras_name = [genre.name for genre in genras]
                tracks_df = pd.concat([tracks_df, pd.DataFrame([{
                    "track_id": track.id,
                    "playlist_name": playlist_name,
                    "artist": track_artist.name,
                    "album": track_album.title,
                    "release_year": track_album.release_date,
                    "genras": genras_name,
                    "related_artists": [artist.name for artist in similar_artists]
                }])], ignore_index=True)
            except :
                pass
    return tracks_df


def  fetch_deezer_tracks_by_name(track_name: str)-> list[any]:
    """
    Fetch Deezer 5 firsts track by name to retreive tracks in front app. The user will select the right one.
    :param track_name:
    :return:
    """
    client = deezer.Client()
    track_list = []
    try:
        results = client.search(track_name)
        for track in results[:5]:
            track_list.append((f"{track.get_artist().name} - {track.title}", track.id))
        return track_list
    except :
        return track_list


def fetch_deezer_track_df(track_id:int)-> pd.DataFrame:
    """
    Fetch Deezer track by id
    :param track id
    :return: df
    """

    df = pd.DataFrame(columns=["track_id", "title", "artist", "album", "release_year", "genras", "related_artists"])

    client = deezer.Client()
    try:
        results = client.get_track(track_id)
        if results:
            track = results
            track_album = track.get_album()
            track_artist = track.get_artist()
            similar_artists = track_artist.get_related()
            genras = track_album.genres
            genras_name = [genre.name for genre in genras]
            df = pd.DataFrame([{
                "track_id": track.id,
                "title": track.title,
                "artist": track_artist.name,
                "album": track_album.title,
                "release_year": track_album.release_date,
                "genras": genras_name,
                "related_artists": [artist.name for artist in similar_artists]}])
        return df
    except :
        print("Error fetching track")
        return df


