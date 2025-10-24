from sklearn.neighbors import KNeighborsClassifier
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from python_scripts.safe_mlb import SafeMLB
from sklearn.model_selection import train_test_split
import pandas as pd
from scipy import sparse
from sklearn.metrics import accuracy_score
import numpy as np

class KnnPlaylist:
    def __init__(self, k=5):
        self.n_neighbors = k
        self.model = None
        self.tfidf_genras = None
        self.multilabel_artists = None
        self.scaler = None
        self.onehot_artist = None
        self.normalizer = None
        self.threshold = None


    def vectorizer_train(self, df : pd.DataFrame) -> tuple[any, any]:
        """
        Vectorize playlist data for training.
        Genres: TF-IDF , Similar Artists: MultiLabelBinarizer, Artist: OneHotEncoder, Release Year: StandardScaler
        :param df: DataFrame containing playlist data
        :return: vectorized documents
        """

        # TF-IDF for genras
        self.tfidf_genras = TfidfVectorizer()
        print(df["genras"])
        genras_doc = [",".join(g) for g in df["genras"]]
        X_genras = self.tfidf_genras.fit_transform(genras_doc)


        # Multi hot for similar artists
        self.multilabel_artists = SafeMLB(sparse_output=True)
        X_sim_artists = self.multilabel_artists.fit_transform(df["related_artists"])


        # One hot for artist
        self.onehot_artist = OneHotEncoder(sparse_output=True, handle_unknown="ignore")
        X_artist = self.onehot_artist.fit_transform(df[["artist"]])

        #numerical features
        self.scaler = StandardScaler()
        X_numerical = self.scaler.fit_transform(df[["release_year"]])
        X_num_sparse = sparse.csr_matrix(X_numerical)

        X = sparse.hstack([X_genras, X_sim_artists, X_artist, X_num_sparse])

        self.normalizer = StandardScaler(with_mean=False)
        X = self.normalizer.fit_transform(X)

        y = df["playlist_name"]

        return X,y

    def vectorizer_pred(self, df : pd.DataFrame) -> list[int]:
        """
        Vectorize the song data for prediction.
        Genres: TF-IDF , Similar Artists: MultiLabelBinarizer, Artist: OneHotEncoder, Release Year: StandardScaler
        :param : df: DataFrame containing song data
        :return: vectorized documents
        """
        # TF-IDF for genras
        genras_doc = [",".join(g) for g in df["genras"]]
        X_genras = self.tfidf_genras.transform(genras_doc)

        # Multi hot for similar artists

        X_sim_artists = self.multilabel_artists.transform(df["related_artists"])

        # One hot for artist
        X_artist = self.onehot_artist.transform(df[["artist"]])

        # numerical features
        X_numerical = self.scaler.transform(df[["release_year"]])
        X_num_sparse = sparse.csr_matrix(X_numerical)

        X = sparse.hstack([X_genras, X_sim_artists,  X_artist, X_num_sparse])
        X = self.normalizer.fit_transform(X)

        return X

    def fit_eval(self, df: pd.DataFrame) -> float:
        """
        Fit the KNN model and predict on test set to evaluate accuracy.
        :param df:
        :return:
        """

        X,y = self.vectorizer_train(df)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

        self.model = KNeighborsClassifier(n_neighbors=2, metric='cosine')
        self.model.fit(X_train, y_train)

        distances, indices = self.model.kneighbors(X)
        mean_distances = distances.mean(axis=1)
        self.threshold = np.percentile(mean_distances, 97)

        y_pred = self.model.predict(X_test)
        return accuracy_score(y_test, y_pred)

    def predict(self, X: list[str]) -> str:
        """
        Predict the playlist name for the given song data.
        :param X:
        :return:
        """
        X = self.vectorizer_pred(X)
        if self.model is None:
            raise Exception("Model has not been fitted yet.")

        prediction = self.model.predict(X)

        distances, indices = self.model.kneighbors(X)
        mean_distances = distances.mean()

        if mean_distances > self.threshold:
            return "unknown"
        else :
            return prediction[0]


    def save_model(self, file_name: str):
        with open(file_name, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load_model(cls,file_name: str) -> object:
        try :
            with open(file_name, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Error loading model from {file_name}: {e}")
            return None
