from python_scripts import get_env_var
from python_scripts import PreparePlaylists

playlist_id = get_env_var("PLAYLIST_ID")

prepare_play = PreparePlaylists()
prepare_play(int(playlist_id))