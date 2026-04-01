def detect_content_type(features: dict):
    """
    Lightweight detection (pre-ML fallback)
    """

    if features.get("code_keywords", 0) > 2:
        return "code", 0.9

    if features.get("text_length", 0) > 200:
        return "document", 0.8

    if features.get("bullet_density", 0) > 2:
        return "slide", 0.75

    return "mixed", 0.6
