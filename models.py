from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
import joblib
import pandas as pd

class EmailClassifier:
    def __init__(self):
        self.model = None
        self.categories = ["Incident", "Request", "Problem"]  

    def train(self, data_path: str):
        """Train and save the classifier"""
        df = pd.read_csv(data_path)
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2))),
            ('clf', LinearSVC(C=0.5))
        ])
        self.model.fit(df['email'], df['type'])
        joblib.dump(self.model, "classifier.joblib")

    def load_model(self):
        """Load pretrained model"""
        self.model = joblib.load("classifier.joblib")
        return self.model
