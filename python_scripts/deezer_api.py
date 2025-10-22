import time
import deezer


def fetch_deezer_playlist(playlist_id: int)-> list[dict]:
    """
    Fetch Deezer playlist tracks and their details.
    :param playlist_id:
    :return:
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
            new_track = {track.id:genras_name}
            list_tracks.append(new_track)
        except :
            time.sleep(3)
            track_album = track.get_album()
            genras = track_album.genres
            genras_name = [genre.name for genre in genras]
            new_track = {track.id: genras_name}
            list_tracks.append(new_track)
    return list_tracks