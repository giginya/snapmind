# snapmind/ml/training.py

import json
import os

import numpy as np

from sklearn.ensemble import RandomForestClassifier
import joblib

MODEL_PATH = "snapmind/ml/model.pkl"
DATA_PATH = "snapmind/ml/data/feedback.json"


def load_training_data():
    if not os.path.exists(DATA_PATH):
        return [], []

    with open(DATA_PATH, "r") as f:
        data = json.load(f)

    X = []
    y = []

    for item in data:
        features = list(item["features"].values())
        label = item["label"]

        X.append(features)
        y.append(label)

    return X, y


def train_model():
    X, y = load_training_data()

    if not X:
        print("No training data available")
        return

    model = RandomForestClassifier()
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)

    print("Model trained and saved")
