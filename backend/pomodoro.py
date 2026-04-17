from fastapi import APIRouter
from pydantic import BaseModel
from backend.database import get_db
from datetime import datetime, timezone

router = APIRouter()

class NameUpdate(BaseModel):
    display_name: str

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
        if row["status"] == 'running' and row["started_at"]:
            elapsed = (datetime.now(timezone.utc) - datetime.fromisoformat(row["started_at"])).total_seconds()
            elapsed += row["pause_elapsed"] or 0
            total = row["duration"] * 60
            progress = min(int((elapsed / total) * 100), 100)
        row["progress"] = progress
        result[user] = row
    return result

@router.post("/pomodoro/{user}/start")
def start_pomodoro(user: str, duration: int = 25): #change minutes for testing timer
    conn = get_db()
    conn.execute(
        "UPDATE pomodoro SET status = 'running', started_at = ?, duration = ?, pause_elapsed = 0 WHERE user = ?",
        (datetime.now(timezone.utc).isoformat(), duration, user)
    )
    conn.commit()
    conn.close()
    return {"status": "ok"}

@router.post("/pomodoro/{user}/pause")
def pause_pomodoro(user: str):
    conn = get_db()
    row = conn.execute("SELECT * FROM pomodoro WHERE user = ?", (user,)).fetchone()
    row = dict(row)
    if row["status"] == "running" and row["started_at"]:
        elapsed = (datetime.now(timezone.utc) - datetime.fromisoformat(row["started_at"])).total_seconds()
        total_elapsed = elapsed + (row["pause_elapsed"] or 0)
        conn.execute(
            "UPDATE pomodoro SET status = 'paused', pause_elapsed = ? WHERE user = ?",
            (total_elapsed, user)
        )
        conn.commit()
    conn.close()
    return {"status": "ok"}

@router.post("/pomodoro/{user}/resume")
def resume_pomodoro(user: str):
    conn = get_db()
    conn.execute(
        "UPDATE pomodoro SET status = 'running', started_at = ? WHERE user = ?",
        (datetime.now(timezone.utc).isoformat(), user)
    )
    conn.commit()
    conn.close()
    return {"status": "ok"}

@router.post("/pomodoro/{user}/stop")
def stop_pomodoro(user: str):
    conn = get_db()
    conn.execute(
        "UPDATE pomodoro SET status = 'idle', started_at = NULL, pause_elapsed = 0 WHERE user = ?",
        (user,)
    )
    conn.commit()
    conn.close()
    return {"status": "ok"}

@router.post("/pomodoro/{user}/complete")
def complete_pomodoro(user: str):
    conn = get_db()
    conn.execute(
        "UPDATE pomodoro SET status = 'idle', started_at = NULL, pause_elapsed = 0, completed_count = completed_count + 1 WHERE user = ?",
        (user,)
    )
    conn.commit()
    conn.close()
    return {"status": "ok"}

@router.patch("/pomodoro/{user}/name")
def update_name(user: str, body: NameUpdate):
    conn = get_db()
    conn.execute(
        "UPDATE pomodoro SET display_name = ? WHERE user = ?",
        (body.display_name, user)
    )
    conn.commit()
    conn.close()
    return {"status": "ok"}

@router.post("/pomodoro/{user}/reset-tomatoes")
def reset_tomatoes(user: str):
    conn = get_db()
    conn.execute("UPDATE pomodoro SET completed_count = 0 WHERE user = ?", (user,))
    conn.commit()
    conn.close()
    return {"status": "ok"}