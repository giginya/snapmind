import datetime


def track_event(event_name: str, user: str | None = None, data: dict | None = None):
    print({
        "event": event_name,
        "user": user,
        "data": data or {},
        "timestamp": str(datetime.datetime.utcnow())
    })
