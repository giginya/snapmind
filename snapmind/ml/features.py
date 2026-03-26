import numpy as np


def detect_code(text: str):
    keywords = ["def", "class", "return", "import", "{", "}"]
    return sum(1 for k in keywords if k in text)


def extract_advanced_features(image, text: str):
    arr = np.array(image)

    return {
        "brightness": float(np.mean(arr)),
        "contrast": float(np.std(arr)),
        "text_length": len(text),
        "line_count": text.count("\n"),
        "uppercase_ratio": (
            sum(1 for c in text if c.isupper()) / max(len(text), 1)
        ),
        "has_numbers": any(c.isdigit() for c in text),
        "bullet_density": text.count("-"),
        "code_keywords": detect_code(text),
    }
