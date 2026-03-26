# snapmind/ml/feedback.py

import json
import os

DATA_PATH = "snapmind/ml/data/feedback.json"


def log_feedback(features, label):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

    data = []

    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            try:
                data = json.load(f)
            except:
                data = []

    data.append({
        "features": features,
        "label": label
    })

    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)
