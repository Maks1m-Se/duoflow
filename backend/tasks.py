from fastapi import APIRouter
from pydantic import BaseModel
from backend.database import get_db

router = APIRouter()

class TaskCreate(BaseModel):
    user: str
    title: str

@router.get("/tasks")
def get_tasks():
    conn = get_db()
    tasks = conn.execute("SELECT * FROM tasks ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(t) for t in tasks]

@router.post("/tasks")
def create_task(task: TaskCreate):
    conn = get_db()
    conn.execute("INSERT INTO tasks (user, title) VALUES (?, ?)", (task.user, task.title))
    conn.commit()
    conn.close()
    return {"status": "ok"}

@router.patch("/tasks/{task_id}/done")
def toggle_task(task_id: int):
    conn = get_db()
    conn.execute("UPDATE tasks SET done = 1 - done WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return {"status": "ok"}

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return {"status": "ok"}