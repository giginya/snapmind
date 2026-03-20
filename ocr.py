import easyocr

# ------------------------------------------------------------
# INITIALIZE OCR READER (once)
# ------------------------------------------------------------
reader = easyocr.Reader(['en'])

# ------------------------------------------------------------
# EXTRACT TEXT
# ------------------------------------------------------------


def extract_text(image_path):

    try:
        results = reader.readtext(image_path)

        text = " ".join([res[1] for res in results])

        return text

    except Exception as e:
        print("OCR Error:", e)
        return ""
