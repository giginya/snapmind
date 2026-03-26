import hashlib
from PIL import Image
import numpy as np

from snapmind.utils.validators import (
    is_valid_image_file,
    is_valid_file_size
)


def validate_image_input(file):
    if not is_valid_image_file(file):
        raise ValueError("Invalid image format")

    if not is_valid_file_size(file):
        raise ValueError("File too large")


def generate_image_hash(file) -> str:
    content = file.getvalue()
    return hashlib.md5(content).hexdigest()


def load_image(file):
    img = Image.open(file)

    return {
        "file": img,
        "width": img.width,
        "height": img.height,
        "format": img.format,
        "size": len(file.getvalue()),
        "hash": generate_image_hash(file),
    }


def preprocess_image(image: dict):
    image["file"] = image["file"].convert("L")
    return image


def clean_extracted_text(text: str) -> str:
    return " ".join(text.split())
