from python_scripts.prepare_playlists import PreparePlaylists
from python_scripts.utils import get_env_var
from python_scripts.knn import KnnPlaylist
import numpy as np

#get and process data

playlists = {'fab': get_env_var("PLAYLIST_FAB_ID"),
             'marg': get_env_var("PLAYLIST_MARG_ID"),
             'max': get_env_var("PLAYLIST_MAX_ID")}

prepare_playlists = PreparePlaylists()

df = prepare_playlists(playlists)


# train model
model = KnnPlaylist(k=2)
accuracy = model.fit_predict(df)

if accuracy > 0.7:
    print(f"Model trained with accuracy: {accuracy}")
    model.save_model("knn_playlist_model.pickle")
else:
    print(f"Model accuracy too low: {accuracy}. Model not saved.")
