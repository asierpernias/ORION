import joblib

MODEL_PATH = "ml/model.pkl"
_model = None

def load_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model

def predict_intent(text: str):
    model = load_model()

    probs = model.predict_proba([text])[0]
    classes = model.classes_

    best_idx = probs.argmax()
    intent = str(classes[best_idx])
    confidence = probs[best_idx]

    return { "intent": intent, "confidence": float(confidence), "text": text, "source": "ml"}
