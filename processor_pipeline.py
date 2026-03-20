from ocr import extract_text
from processor import clean_text
from storage import save_note


def process_image(image_path):

    raw_text = extract_text(image_path)

    # SAFETY CHECK
    if not raw_text or len(raw_text.strip()) < 5:
        return None

    cleaned_text = clean_text(raw_text)

    save_note(cleaned_text, image_path)

    return cleaned_text
