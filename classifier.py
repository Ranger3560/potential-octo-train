from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
import joblib
import pandas as pd

class EmailClassifier:
    def __init__(self):
        self.model = None
        self.categories = ["Incident", "Request"]  # Update per your dataset
    
    def train(self, data_path: str):
        df = pd.read_csv(data_path)
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('clf', LinearSVC())
        ])
        self.model.fit(df['email'], df['type'])
    
    def predict(self, text: str) -> str:
        return self.model.predict([text])[0]
    
    def save(self, path: str):
        joblib.dump(self.model, path)
    
    def load(self, path: str):
        self.model = joblib.load(path)
