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

def fetch_deezer_track(track_name: str)-> pd.DataFrame:
    """
    Fetch Deezer track genras.
    :param track name:
    :return: df
    """

    df = pd.DataFrame(columns=["track_id", "artist", "album", "release_year", "genras", "related_artists"])

    client = deezer.Client()
    try:
        results = client.search(track_name)
        if results:
            track = results[0]
            track_album = track.get_album()
            track_artist = track.get_artist()
            similar_artists = track_artist.get_related()
            genras = track_album.genres
            genras_name = [genre.name for genre in genras]
            df = pd.DataFrame([{
                "track_id": track.id,
                "artist": track_artist.name,
                "album": track_album.title,
                "release_year": track_album.release_date,
                "genras": genras_name,
                "related_artists": [artist.name for artist in similar_artists]}])
    except Exception as e:
        print(f"Error fetching track {track_name}: {e}")
        return df

    return df
