import pytesseract


def extract_text(image: dict, mode: str):
    """
    OCR extraction layer
    """

    try:
        text = pytesseract.image_to_string(image["file"])
        return text, 0.8

    except Exception:
        return "", 0.0
