# snapmind/storage/cloud/sheets.py

import json
import time
from typing import List

from snapmind.storage.local.store import serialize_note

try:
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
except ImportError:
    gspread = None


CREDENTIALS_PATH = "config/credentials.json"
SHEET_NAME = "SnapMindDB"
MAX_RETRIES = 3


def _get_client():
    if gspread is None:
        raise ImportError("gspread not installed")

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_PATH, scope
    )

    return gspread.authorize(creds)


def _get_sheet():
    client = _get_client()

    try:
        return client.open(SHEET_NAME).sheet1
    except Exception:
        return client.create(SHEET_NAME).sheet1


def _note_to_row(note_dict: dict) -> List[str]:
    return [
        note_dict["id"],
        note_dict["title"],
        note_dict["summary"],
        json.dumps(note_dict["blocks"]),
        note_dict["created_at"],
        note_dict["type"],
        ",".join(note_dict["tags"]),
        json.dumps(note_dict["metadata"]),
    ]


def push_note_to_sheets(note):
    sheet = _get_sheet()
    data = serialize_note(note)
    row = _note_to_row(data)

    for attempt in range(MAX_RETRIES):
        try:
            sheet.append_row(row)
            return True
        except Exception as e:
            if attempt == MAX_RETRIES - 1:
                raise e
            time.sleep(2 ** attempt)

    return False
