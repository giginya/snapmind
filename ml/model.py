# ml/model.py

import os
import joblib

MODEL_PATH = "ml/model.pkl"


def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    return joblib.load(MODEL_PATH)


def predict(features: dict):
    model = load_model()

    if model:
        return model.predict([list(features.values())])[0]

    # fallback
    if features["text_length"] > 200:
        return "document"
    if features["code_keywords"] > 2:
        return "code"

    return "mixed"
