import datetime


class SnapMindError(Exception):
    def __init__(self, message: str, context: dict | None = None):
        super().__init__(message)
        self.message = message
        self.context = context or {}
        self.timestamp = str(datetime.datetime.utcnow())


def track_error(error: Exception, context: dict | None = None):
    print({
        "type": type(error).__name__,
        "message": str(error),
        "context": context or {},
        "timestamp": str(datetime.datetime.utcnow())
    })
