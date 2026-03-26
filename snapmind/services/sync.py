# snapmind/services/sync.py

import json
import os
import time

from snapmind.storage.local.store import save_note
from snapmind.storage.cloud.sheets import push_note_to_sheets


QUEUE_PATH = "snapmind/storage/cloud/queue.json"


def _load_queue():
    if not os.path.exists(QUEUE_PATH):
        return []

    with open(QUEUE_PATH, "r") as f:
        try:
            return json.load(f)
        except:
            return []


def _save_queue(queue):
    os.makedirs(os.path.dirname(QUEUE_PATH), exist_ok=True)

    with open(QUEUE_PATH, "w") as f:
        json.dump(queue, f, indent=2)


def _enqueue(note_dict):
    queue = _load_queue()
    queue.append(note_dict)
    _save_queue(queue)


def _flush_queue():
    queue = _load_queue()
    remaining = []

    for item in queue:
        try:
            push_note_to_sheets(item)
        except Exception:
            remaining.append(item)

    _save_queue(remaining)


def save_and_sync(note):
    # 1. always save locally
    save_note(note)

    # 2. attempt cloud sync
    try:
        push_note_to_sheets(note)
    except Exception:
        _enqueue(note.__dict__)

    # 3. background retry
    try:
        _flush_queue()
    except Exception:
        pass
