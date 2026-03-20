import easyocr


def extract_text(image_path):

    try:
        reader = easyocr.Reader(['en'], gpu=False)

        results = reader.readtext(image_path)

        if not results:
            return ""

        texts = []

        for item in results:
            # item structure: [bbox, text, confidence]
            if isinstance(item, (list, tuple)) and len(item) >= 2:
                texts.append(str(item[1]))

        return " ".join(texts)

    except Exception as e:
        print("OCR Error:", e)
        return ""
