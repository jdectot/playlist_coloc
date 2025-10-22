import time
import deezer


def fetch_deezer_playlist(playlist_id: int)-> list[list[str]]:
    """
    Fetch Deezer playlist tracks and their details.
    :param playlist_id:
    :return:[{track_id: [genra1, genra2,...]},...]
    """

    client = deezer.Client()
    list_tracks = []

    try:
        playlists = client.get_playlist(playlist_id)
    except Exception as e:
        print(f"Error fetching playlist {playlist_id}: {e}")
        return list_tracks

    for track in playlists.tracks:
        try :
            track_album = track.get_album()
            genras = track_album.genres
            genras_name = [genre.name for genre in genras]
            list_tracks.append(genras_name)

        except :
            time.sleep(3)
            try :
                track_album = track.get_album()
                genras = track_album.genres
                genras_name = [genre.name for genre in genras]
                list_tracks.append(genras_name)
            except :
                pass
    return list_tracks

def fetch_deezer_track(track_name: str)-> list[str]:
    """
    Fetch Deezer track genras.
    :param track name:
    :return: [genra1, genra2,...]
    """

    client = deezer.Client()
    genras_name = []
    try:
        results = client.search(track_name)
        print(results)
        if results:
            track = results[0]
            track_album = track.get_album()
            genras = track_album.genres
            genras_name = [genre.name for genre in genras]
    except Exception as e:
        print(f"Error fetching track {track_name}: {e}")
        return genras_name

    return genras_name
