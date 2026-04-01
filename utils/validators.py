import re
from storage.schema import Note


MAX_FILE_SIZE_MB = 5
SUPPORTED_FORMATS = ["jpg", "jpeg", "png"]


def is_valid_email(email: str) -> bool:
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))


def is_valid_otp(otp: str) -> bool:
    return otp.isdigit() and len(otp) == 6


def is_valid_image_file(file) -> bool:
    if file is None:
        return False

    filename = file.name.lower()
    return any(filename.endswith(ext) for ext in SUPPORTED_FORMATS)


def is_valid_file_size(file, max_size_mb: int = MAX_FILE_SIZE_MB) -> bool:
    return len(file.getvalue()) <= max_size_mb * 1024 * 1024


def clean_text_input(text: str) -> str:
    return text.strip()


def normalize_search_query(query: str) -> str:
    return query.lower().strip()


def validate_note(note: Note):
    if not note.title:
        raise ValueError("Note must have title")

    if note.blocks is None:
        raise ValueError("Note must have blocks")

    if note.metadata is None:
        raise ValueError("Note must have metadata")
