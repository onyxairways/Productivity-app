from sqlalchemy.orm import Session
from .database import TaskDB
from .models import TaskCreate

def get_tasks(db: Session):
    return db.query(TaskDB).all()

def get_task(db: Session, task_id: int):
    return db.query(TaskDB).filter(TaskDB.id == task_id).first()

def create_task(db: Session, task: TaskCreate):
    db_task = TaskDB(title=task.title, description=task.description)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, completed: bool):
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if db_task:
        db_task.completed = completed
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task
