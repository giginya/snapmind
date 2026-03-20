from ocr import extract_text
from processor import clean_text
from storage import save_note

# ------------------------------------------------------------
# FULL PROCESSING PIPELINE
# ------------------------------------------------------------


def process_image(image_path):

    # Step 1: OCR
    raw_text = extract_text(image_path)

    if not raw_text:
        return ""

    # Step 2: Clean
    cleaned_text = clean_text(raw_text)

    # Step 3: Save
    save_note(cleaned_text, image_path)

    return cleaned_text
