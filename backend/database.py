import sqlite3

def get_db():
    conn = sqlite3.connect("duoflow.db")
    conn.row_factory = sqlite3.Row  # gibt Ergebnisse als Dictionary zurück
    return conn

def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            title TEXT NOT NULL,
            done INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS pomodoro (
            user TEXT PRIMARY KEY,
            status TEXT DEFAULT 'idle',
            started_at TEXT,
            duration INTEGER DEFAULT 25
        );

        INSERT OR IGNORE INTO pomodoro (user) VALUES ('user1');
        INSERT OR IGNORE INTO pomodoro (user) VALUES ('user2');
    """)
    conn.commit()
    conn.close()