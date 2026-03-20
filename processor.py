# ------------------------------------------------------------
# PURPOSE:
# Clean OCR output
# ------------------------------------------------------------

def clean_text(text):

    lines = text.split("\n")

    cleaned = []

    for line in lines:
        line = line.strip()

        # Remove empty/noise lines
        if len(line) > 2:
            cleaned.append(line)

    return "\n".join(cleaned)
