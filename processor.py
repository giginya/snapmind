def clean_text(text):

    if not text:
        return ""

    lines = text.split("\n")

    cleaned = []

    for line in lines:
        line = line.strip()

        if len(line) > 2:
            cleaned.append(line)

    return "\n".join(cleaned)
