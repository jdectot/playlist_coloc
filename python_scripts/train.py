from prepare_playlists import PreparePlaylists
from utils import get_env_var
from knn import KnnPlaylist
import numpy as np

#get and process data

playlists = {'fab': get_env_var("PLAYLIST_FAB_ID"),
             'marg': get_env_var("PLAYLIST_MARG_ID"),
             'max': get_env_var("PLAYLIST_MAX_ID")}

prepare_playlists = PreparePlaylists()
X, y = prepare_playlists(playlists)




# train model
model = KnnPlaylist(k=2)
model.fit(X, y)
model.save_model("knn_playlist_model.pickle")
