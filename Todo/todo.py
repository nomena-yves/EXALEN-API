from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn


app = FastAPI(title="To-Do List API", description="Une API simple pour gérer une liste de tâches")


class Task(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool = False


tasks_db = []


@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    return tasks_db


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    for task in tasks_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Tâche non trouvée")


@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    for existing_task in tasks_db:
        if existing_task.id == task.id:
            raise HTTPException(status_code=400, detail="Une tâche avec cet ID existe déjà")
    tasks_db.append(task)
    return task


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(tasks_db):
        if task.id == task_id:
            tasks_db[index] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Tâche non trouvée")


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    for index, task in enumerate(tasks_db):
        if task.id == task_id:
            tasks_db.pop(index)
            return {"message": "Tâche supprimée avec succès"}
    raise HTTPException(status_code=404, detail="Tâche non trouvée")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)