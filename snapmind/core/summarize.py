# snapmind/core/summarize.py

from datetime import datetime
from snapmind.storage.schema import Note, ProcessingMetadata


def generate_title(text: str):
    return text.split(".")[0][:50] if text else "Untitled"


def generate_summary(text: str):
    return text[:200] if text else ""


def generate_tags(text: str):
    words = text.lower().split()
    return list(set(words[:5]))


def summarize_content(blocks):
    text = " ".join([b.content for b in blocks])

    now = str(datetime.utcnow())

    # 🔴 FIX: NEVER use None for metadata
    dummy_metadata = ProcessingMetadata(
        detected_type="unknown",
        confidence=0.0,
        ocr_confidence=0.0,
        processing_mode="init",
    )

    return Note(
        id="",
        title=generate_title(text),
        summary=generate_summary(text),
        blocks=blocks,
        created_at=now,
        updated_at=now,
        type="text",
        tags=generate_tags(text),
        image={},
        metadata=dummy_metadata,   # ✅ FIXED
    )


def build_processing_metadata(detected_type, confidence, ocr_conf, mode):
    return ProcessingMetadata(
        detected_type=detected_type,
        confidence=confidence,
        ocr_confidence=ocr_conf,
        processing_mode=mode,
    )


def finalize_note(note, metadata):
    note.metadata = metadata
    return note
