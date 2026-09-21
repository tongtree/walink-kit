import os
import sqlite3
from collections.abc import Generator

DEFAULT_URL = "sqlite:///./links.sqlite3"


def database_path() -> str:
    url = os.getenv("DATABASE_URL", DEFAULT_URL)
    if url.startswith("sqlite:///"):
        return url.replace("sqlite:///", "", 1)
    raise RuntimeError("This demo only supports sqlite DATABASE_URL values.")


def get_db() -> Generator[sqlite3.Connection, None, None]:
    connection = sqlite3.connect(database_path())
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def init_db() -> None:
    connection = sqlite3.connect(database_path())
    try:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                slug TEXT UNIQUE NOT NULL,
                phone TEXT NOT NULL,
                message TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
            );
            CREATE TABLE IF NOT EXISTS clicks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                link_id INTEGER NOT NULL,
                ip TEXT NOT NULL DEFAULT '',
                referer TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
            );
            """
        )
        connection.commit()
    finally:
        connection.close()
