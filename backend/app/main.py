import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import anthropic

load_dotenv()

from . import database, crud
from .models import TaskCreate, TaskResponse, TaskDescriptionUpdate, SuggestRequest


database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "message": "Backend running"}


@app.get("/tasks", response_model=List[TaskResponse])
def read_tasks(db: Session = Depends(database.get_db)):
    return crud.get_tasks(db)


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, db: Session = Depends(database.get_db)):
    task = crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(database.get_db)):
    return crud.create_task(db, task)


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, completed: bool, db: Session = Depends(database.get_db)):
    task = crud.update_task(db, task_id, completed)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.delete("/tasks/{task_id}", response_model=TaskResponse)
def delete_task(task_id: int, db: Session = Depends(database.get_db)):
    task = crud.delete_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task_description(
    task_id: int, update: TaskDescriptionUpdate, db: Session = Depends(database.get_db)
):
    task = crud.update_description(db, task_id, update.description)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks/{task_id}/questions")
def get_questions(task_id: int, db: Session = Depends(database.get_db)):
    task = crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=128,
        messages=[
            {
                "role": "user",
                "content": f"I have a task called '{task.title}'. Write exactly 2 short clarifying questions to help write a better description. Each question must be under 10 words. Return them as a numbered list, nothing else.",
            }
        ],
    )

    lines = [
        l.strip() for l in message.content[0].text.strip().split("\n") if l.strip()
    ]
    questions = []
    for line in lines:
        cleaned = line.lstrip("0123456789.)- ").strip()
        if cleaned:
            questions.append(cleaned)

    return {"questions": questions[:2]}


@app.post("/tasks/{task_id}/suggest")
def suggest_description(
    task_id: int, request: SuggestRequest = None, db: Session = Depends(database.get_db)
):
    task = crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    answers_text = ""
    if request and request.answers:
        answers_text = " Additional context: " + " ".join(request.answers)

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        messages=[
            {
                "role": "user",
                "content": f"You are a productivity assistant. The task is: '{task.title}'.{answers_text}\n\nLook at what kind of task this is and respond appropriately:\n- If it involves writing something (email, message, letter) → provide a ready-to-use draft they can send directly\n- If it involves doing something step by step → provide clear numbered steps\n- Otherwise → write a short 2-3 sentence description of what needs to be done\n\nBe immediately useful. Plain text only, no markdown headers.",

            }
        ],
    )

    suggestion = message.content[0].text
    return {"suggestion": suggestion}
