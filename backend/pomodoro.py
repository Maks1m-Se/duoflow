from fastapi import APIRouter
from backend.database import get_db
from datetime import datetime, timezone

router = APIRouter()

@router.get("/pomodoro")
def get_pomodoro():
    conn = get_db()
    rows = conn.execute("SELECT * FROM pomodoro").fetchall()
    conn.close()
    result = {}
    for row in rows:
        row = dict(row)
        user = row["user"]
        progress = 0
        if row["status"] == "running" and row["started_at"]:
            elapsed = (datetime.now(timezone.utc) - datetime.fromisoformat(row["started_at"])).total_seconds()
            total = row["duration"] * 60
            progress = min(int((elapsed / total) * 100), 100)
        row["progress"] = progress
        result[user] = row
    return result

@router.post("/pomodoro/{user}/start")
def start_pomodoro(user: str, duration: int = 25):
    conn = get_db()
    conn.execute(
        "UPDATE pomodoro SET status = 'running', started_at = ?, duration = ? WHERE user = ?",
        (datetime.now(timezone.utc).isoformat(), duration, user)
    )
    conn.commit()
    conn.close()
    return {"status": "ok"}

@router.post("/pomodoro/{user}/stop")
def stop_pomodoro(user: str):
    conn = get_db()
    conn.execute(
        "UPDATE pomodoro SET status = 'idle', started_at = NULL WHERE user = ?",
        (user,)
    )
    conn.commit()
    conn.close()
    return {"status": "ok"}