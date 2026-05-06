import uuid


def unique_text(prefix: str) -> str:
    return f"{prefix} {uuid.uuid4().hex[:8]}"
