from sklearn.neighbors import KNeighborsClassifier
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer, OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import pandas as pd
from scipy import sparse
from sklearn.metrics import accuracy_score

class KnnPlaylist:
    def __init__(self, k=5):
        self.n_neighbors = k
        self.model = None
        self.tfidf_genras = None
        self.multilabel_artists = None
        self.scaler = None
        self.onehot_artist = None


    def vectorizer_train(self, df : pd.DataFrame) -> list[list[int]]:
        """
        Vectorize the documents using TF-IDF.
        :param docs: list of documents
        :return: vectorized documents
        """

        # TF-IDF for genras
        self.tfidf_genras = TfidfVectorizer()
        print(df["genras"])
        genras_doc = [",".join(g) for g in df["genras"]]
        X_genras = self.tfidf_genras.fit_transform(genras_doc)
        print("One example of TF-IDF genras vectorization:")
        print(X_genras.toarray()[0])

        # Multi hot for similar artists
        self.multilabel_artists = MultiLabelBinarizer(sparse_output=True)
        X_sim_artists = self.multilabel_artists.fit_transform(df["related_artists"])
        print("One example of MultiLabelBinarizer similar artists vectorization:")
        print(X_sim_artists.toarray()[0])

        # One hot for artist
        self.onehot_artist = OneHotEncoder(sparse_output=True)
        X_artist = self.onehot_artist.fit_transform(df[["artist"]])
        print("One example of OneHotEncoder artist vectorization:")
        print(X_artist.toarray()[0])

        #numerical features
        self.scaler = StandardScaler()
        X_numerical = self.scaler.fit_transform(df[["release_year"]])
        X_num_sparse = sparse.csr_matrix(X_numerical)
        print("One example of StandardScaler numerical vectorization:")
        print(X_num_sparse.toarray()[0])

        X = sparse.hstack([X_genras, X_sim_artists, X_artist, X_num_sparse])

        print("Shape finale du vecteur :", X)
        print("Type :", type(X))
        y = df["playlist_name"]

        return X,y

    def vectorizer_pred(self, df : pd.DataFrame) -> list[list[int]]:
        """
        Vectorize the documents using the trained TF-IDF vectorizer.
        :param docs: list of documents
        :return: vectorized documents
        """


    def fit(self, df: pd.DataFrame):
        X,y = self.vectorizer_train(df)

        self.model = KNeighborsClassifier(n_neighbors=self.n_neighbors)
        self.model.fit(X, y)

    def fit_predict(self, df: pd.DataFrame) -> float:
        X,y = self.vectorizer_train(df)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

        self.model = KNeighborsClassifier(n_neighbors=2, metric='cosine')
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        return accuracy_score(y_test, y_pred)

    def predict(self, X: list[str]) -> list[str]:
        X = self.vectorizer_pred(X)
        if self.model is None:
            raise Exception("Model has not been fitted yet.")
        return self.model.predict(X)

    def save_model(self, file_name: str):
        with open(file_name, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load_model(self, file_name: str) -> object:
        with open(file_name, "rb") as f:
            return pickle.load(f)
