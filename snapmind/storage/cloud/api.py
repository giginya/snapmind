# snapmind/storage/cloud/api.py

class CloudAPI:
    """
    Abstract interface for cloud storage.
    Future-ready for:
    - Google Sheets
    - Firebase
    - REST APIs
    """

    def push_note(self, note: dict):
        raise NotImplementedError

    def fetch_notes(self):
        raise NotImplementedError
