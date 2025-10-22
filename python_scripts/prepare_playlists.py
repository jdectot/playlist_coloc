from sklearn.feature_extraction.text import TfidfVectorizer
from deezer_api import fetch_deezer_playlist
import pandas as pd



class PreparePlaylists:
    def __init__(self):
        self.playlist_tracks= list()
        self.character = list()
        self.vectorized_playlist = list()


    def __call__(self, playlist_ids: dict) -> tuple[list, list]:

        train_df = pd.DataFrame(columns=["track_id", "playlist_name", "artist", "album", "release_year", "genras","related_artists"])

        for name,id in playlist_ids.items():

            df = fetch_deezer_playlist(id,name)
            train_df = pd.concat([train_df, df], ignore_index=True)

        train_df = self.data_cleaning(train_df)


        return train_df


    @staticmethod
    def data_cleaning(train_df: pd.DataFrame) -> pd.DataFrame:
        # add empty list for missing genras or related artists
        train_df["genras"] = train_df["genras"].apply(lambda x: x if isinstance(x, list) else [])
        train_df["related_artists"] = train_df["related_artists"].apply(lambda x: x if isinstance(x, list) else [])

        # clean genras and related artists column
        for ix, row in train_df.iterrows():
            train_df.at[ix, "genras"] = clean_list(row["genras"])

            train_df.at[ix, "related_artists"] = clean_list(row["related_artists"])

        # get only year from release date
        train_df["release_year"] = pd.to_datetime(train_df["release_year"], errors='coerce').dt.year.fillna(0).astype(
            int)

        return train_df


def clean_list(df_list):
    return [g.replace(" ", "_") for g in df_list]
