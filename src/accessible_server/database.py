from __future__ import annotations

import os
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from platformdirs import user_data_dir


def data_dir() -> Path:
    override = os.environ.get("ACCESSIBLE_SERVER_DATA_DIR")
    root = Path(override) if override else Path(user_data_dir("AccessibleServer", "ejjjkkjlkkj"))
    root.mkdir(parents=True, exist_ok=True)
    return root


def database_path() -> Path:
    return data_dir() / "accessible-server.db"


def connect() -> sqlite3.Connection:
    connection = sqlite3.connect(database_path())
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA journal_mode=WAL")
    connection.execute("PRAGMA foreign_keys=ON")
    return connection


def initialize() -> None:
    with connect() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS event_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                level TEXT NOT NULL,
                message TEXT NOT NULL
            )
            """
        )


def add_event(message: str, level: str = "info") -> None:
    initialize()
    with connect() as connection:
        connection.execute(
            "INSERT INTO event_log(created_at, level, message) VALUES (?, ?, ?)",
            (datetime.now(UTC).isoformat(), level, message),
        )


def recent_events(limit: int = 20) -> list[dict[str, str | int]]:
    initialize()
    safe_limit = max(1, min(limit, 100))
    with connect() as connection:
        rows = connection.execute(
            "SELECT id, created_at, level, message FROM event_log ORDER BY id DESC LIMIT ?",
            (safe_limit,),
        ).fetchall()
    return [dict(row) for row in rows]
