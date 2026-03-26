import json
import os

from snapmind.storage.schema import Note, Block, ProcessingMetadata
from snapmind.utils.validators import validate_note


DB_PATH = "storage/local/db.json"


def ensure_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w") as f:
            json.dump([], f)


def serialize_note(note: Note):
    return {
        "id": note.id,
        "title": note.title,
        "summary": note.summary,
        "blocks": [
            {"type": b.type, "content": b.content, "metadata": b.metadata}
            for b in note.blocks
        ],
        "created_at": note.created_at,
        "updated_at": note.updated_at,
        "type": note.type,
        "tags": note.tags,
        "image": note.image,
        "metadata": vars(note.metadata),
    }


def deserialize_note(data: dict):
    blocks = [Block(**b) for b in data["blocks"]]
    metadata = ProcessingMetadata(**data["metadata"])

    return Note(
        id=data["id"],
        title=data["title"],
        summary=data["summary"],
        blocks=blocks,
        created_at=data["created_at"],
        updated_at=data["updated_at"],
        type=data["type"],
        tags=data["tags"],
        image=data["image"],
        metadata=metadata,
    )


def load_notes():
    ensure_db()

    with open(DB_PATH, "r") as f:
        data = json.load(f)

    return [deserialize_note(d) for d in data]


def save_note(note: Note):
    validate_note(note)

    notes = load_notes()
    notes.append(note)

    with open(DB_PATH, "w") as f:
        json.dump([serialize_note(n) for n in notes], f, indent=2)


def search_notes(query: str):
    query = query.lower()

    results = []

    for note in load_notes():
        if query in note.title.lower() or query in note.summary.lower():
            results.append(note)

    return results
