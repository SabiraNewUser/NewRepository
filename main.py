from pydantic import BaseModel
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: str
    completed: bool

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskInDB(TaskBase):
    id: int

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# In-memory database
tasks_db = {}
counter = 1

class TaskBase(BaseModel):
    title: str
    description: str
    completed: bool

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskInDB(TaskBase):
    id: int

@app.get("/tasks", response_model=List[TaskInDB])
def get_tasks():
    return list(tasks_db.values())

@app.get("/tasks/{task_id}", response_model=TaskInDB)
def get_task(task_id: int):
    task = tasks_db.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks", response_model=TaskInDB)
def create_task(task: TaskCreate):
    global counter
    new_task = TaskInDB(id=counter, **task.dict())
    tasks_db[counter] = new_task
    counter += 1
    return new_task

@app.put("/tasks/{task_id}", response_model=TaskInDB)
def update_task(task_id: int, task: TaskUpdate):
    existing_task = tasks_db.get(task_id)
    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    updated_task = existing_task.copy(update=task.dict(exclude_unset=True))
    tasks_db[task_id] = updated_task
    return updated_task

@app.delete("/tasks/{task_id}", response_model=TaskInDB)
def delete_task(task_id: int):
    task = tasks_db.pop(task_id, None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
