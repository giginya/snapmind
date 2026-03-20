import easyocr

# ------------------------------------------------------------
# SAFE OCR (LAZY LOAD)
# ------------------------------------------------------------


def extract_text(image_path):

    try:
        # Load reader only when needed (prevents startup crash)
        reader = easyocr.Reader(['en'], gpu=False)

        results = reader.readtext(image_path)

        if not results:
            return ""

        text = " ".join([res[1] for res in results])

        return text

    except Exception as e:
        print("OCR Error:", e)
        return ""
