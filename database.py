import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "instance" / "database.db"


def get_db():
    DATABASE_PATH.parent.mkdir(exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS attendees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                organization TEXT NOT NULL,
                city TEXT NOT NULL,
                category TEXT NOT NULL,
                event TEXT NOT NULL,
                registration_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                checked_in INTEGER NOT NULL DEFAULT 0,
                checkin_time TEXT,
                qr_token TEXT NOT NULL UNIQUE
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS venues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                city TEXT NOT NULL,
                capacity INTEGER NOT NULL,
                cost REAL NOT NULL DEFAULT 0,
                amenities TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                speaker_name TEXT NOT NULL,
                speaker_email TEXT,
                venue_id INTEGER NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                capacity INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'Scheduled',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (venue_id) REFERENCES venues(id)
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS speakers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                organization TEXT,
                expertise TEXT,
                availability TEXT NOT NULL,
                bio TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                message TEXT NOT NULL,
                audience TEXT NOT NULL,
                recipient_count INTEGER NOT NULL DEFAULT 0,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS agent_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_name TEXT NOT NULL,
                run_type TEXT NOT NULL,
                status TEXT NOT NULL,
                summary TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.execute("CREATE INDEX IF NOT EXISTS idx_attendees_event ON attendees(event)")
        db.execute("CREATE INDEX IF NOT EXISTS idx_attendees_checkin ON attendees(checked_in)")
        db.execute("CREATE INDEX IF NOT EXISTS idx_sessions_time ON sessions(start_time, end_time)")
        db.execute("CREATE INDEX IF NOT EXISTS idx_agent_runs_created ON agent_runs(created_at)")
        session_columns = {row["name"] for row in db.execute("PRAGMA table_info(sessions)").fetchall()}
        if "speaker_id" not in session_columns:
            db.execute("ALTER TABLE sessions ADD COLUMN speaker_id INTEGER")
