from sklearn.neighbors import KNeighborsClassifier
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

class KnnPlaylist:
    def __init__(self, k=5):
        self.n_neighbors = k
        self.model = None
        self.vectorizer = None


    def vectorizer_train(self, docs: list[str]) -> list[list[int]]:
        """
        Vectorize the documents using TF-IDF.
        :param docs: list of documents
        :return: vectorized documents
        """
        self.vectorizer = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b")
        X = self.vectorizer.fit_transform(docs)
        return X.toarray()

    def vectorizer_pred(self, docs: list[str]) -> list[list[int]]:
        """
        Vectorize the documents using the trained TF-IDF vectorizer.
        :param docs: list of documents
        :return: vectorized documents
        """
        X = self.vectorizer.transform(docs)
        return X.toarray()

    def fit(self, X, y):
        X = self.vectorizer_train(X)
        # print vectorized X
        for row in X:
            print(row)
        self.model = KNeighborsClassifier(n_neighbors=self.n_neighbors)
        self.model.fit(X, y)

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