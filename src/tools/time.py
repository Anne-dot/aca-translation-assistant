from datetime import datetime


def current_time() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")
