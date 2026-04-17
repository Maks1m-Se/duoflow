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
            display_name TEXT,
            status TEXT DEFAULT 'idle',
            started_at TEXT,
            pause_elapsed INTEGER DEFAULT 0,
            duration INTEGER DEFAULT 25,
            completed_count INTEGER DEFAULT 0
        );

        INSERT OR IGNORE INTO pomodoro (user, display_name) VALUES ('user1', 'Maksim');
        INSERT OR IGNORE INTO pomodoro (user, display_name) VALUES ('user2', 'Freundin');
    """)
    # Neue Spalten hinzufügen falls DB schon existiert
    try:
        conn.execute("ALTER TABLE pomodoro ADD COLUMN display_name TEXT")
    except: pass
    try:
        conn.execute("ALTER TABLE pomodoro ADD COLUMN pause_elapsed INTEGER DEFAULT 0")
    except: pass
    try:
        conn.execute("ALTER TABLE pomodoro ADD COLUMN completed_count INTEGER DEFAULT 0")
    except: pass
    conn.commit()
    conn.close()