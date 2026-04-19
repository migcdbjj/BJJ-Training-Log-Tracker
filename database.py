import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "bjj_log.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS sessions (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            date            TEXT NOT NULL,
            duration        INTEGER NOT NULL,
            session_type    TEXT NOT NULL,
            rounds          INTEGER,
            intensity       INTEGER NOT NULL,
            feeling_before  INTEGER NOT NULL,
            feeling_after   INTEGER NOT NULL,
            notes           TEXT
        );
        
        CREATE TABLE IF NOT EXISTS tags (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            name            TEXT NOT NULL UNIQUE,
            tag_type        TEXT
        );
        
        CREATE TABLE IF NOT EXISTS session_tags (
            session_id          INTEGER NOT NULL,
            tag_id              INTEGER NOT NULL,
            context             TEXT NOT NULL,
            PRIMARY KEY (session_id, tag_id, context),
            FOREIGN KEY (session_id) REFERENCES sessions (id),
            FOREIGN KEY (tag_id) REFERENCES tags (id)
        );    
    """)
    conn.commit()
    conn.close()
    print("Database initialized.")
    print(f"File size: {os.path.getsize(DB_PATH)} bytes")


if __name__ == "__main__":
    initialize_db()