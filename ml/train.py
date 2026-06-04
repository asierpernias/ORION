import json
import joblib
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.pipeline import Pipeline
from logger import log

DATA_PATH = "ml/training_data.json"
MODEL_PATH = "ml/model.pkl"

def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    x = [item["text"] for item in data]
    y = [item["intent"] for item in data]
    return x, y
def train():
    x, y = load_data()

    log.info(Counter(y))
    log.info(min(Counter(y).values()))

    base = Pipeline ([
        ("tfidf", TfidfVectorizer(ngram_range=(1,2))),
        ("clf", LinearSVC())
    ])

    model = CalibratedClassifierCV(base, method="sigmoid")
    model.fit(x, y)

    joblib.dump(model, MODEL_PATH)

    log.info("Model entrendado")

if __name__ == "__main__":
    
    train()
    