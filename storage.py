import os
from datetime import datetime


def save_note(text, image_path):

    if not text:
        return

    os.makedirs("notes", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_path = f"notes/note_{timestamp}.txt"

    with open(file_path, "w") as f:
        f.write("SnapMind Note\n\n")
        f.write("Content:\n")
        f.write(text + "\n\n")
        f.write(f"Source: {image_path}")
