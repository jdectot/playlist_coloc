from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np
import scipy.sparse as sp

class SafeMLB(MultiLabelBinarizer):
    def transform(self, y):
        # Filtrer les valeurs inconnues
        y_filtered = [
            [label for label in labels if label in self.classes_]
            for labels in y
        ]
        return super().transform(y_filtered)