from utils import get_env_var
from prepare_playlists import PreparePlaylists

playlist_id = get_env_var("PLAYLIST_ID")

prepare_play = PreparePlaylists()
prepare_play(int(playlist_id))