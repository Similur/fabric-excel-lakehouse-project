"""Helpers for testing the demo's column, timestamp, and overlap rules."""

from __future__ import annotations

from datetime import datetime, timezone

REQUIRED_COLUMNS = {"record_id", "activity_date", "amount", "updated_at"}


def validate_columns(columns: list[str]) -> None:
    """Check that the source includes all required columns."""
    missing = REQUIRED_COLUMNS - set(columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")


def parse_utc(value: str) -> datetime:
    """Convert an ISO timestamp to UTC, rejecting values without a timezone."""
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("updated_at must include a timezone")
    return parsed.astimezone(timezone.utc)


def newest_records(rows: list[dict]) -> list[dict]:
    """Keep the newest version of each record, even when reports overlap."""
    latest: dict[str, dict] = {}
    for row in rows:
        validate_columns(list(row))
        record_id = str(row["record_id"]).strip()
        if not record_id:
            raise ValueError("record_id cannot be blank")
        updated_at = parse_utc(str(row["updated_at"]))
        current = latest.get(record_id)
        if current is None or updated_at > parse_utc(str(current["updated_at"])):
            latest[record_id] = dict(row)
    return [latest[key] for key in sorted(latest)]
