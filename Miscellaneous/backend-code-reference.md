# Backend Code Reference

Plain-language breakdown of every backend file — what each file is for, what each part does,
and how the files connect to each other.

Updated automatically as new files are added.

================================================================================
HOW THE FILES FIT TOGETHER (overview)
================================================================================

  main.py          ← entry point. FastAPI app lives here. Receives HTTP requests,
                     calls crud.py functions, returns responses.
                     Imports from: database.py, models.py, crud.py

  models.py        ← defines the shape of data for the API (Pydantic).
                     Used by main.py to validate what comes IN and what goes OUT.
                     Does not talk to the database directly.

  database.py      ← sets up the SQLite connection and defines the database table (SQLAlchemy).
                     Used by main.py (to get a db session) and crud.py (to run queries).

  crud.py          ← contains the database logic: create, read, update, delete.
                     Called by main.py. Uses models.py for input types, database.py for the table.

  Request flow:
  Browser/Angular → main.py (receives request) → crud.py (database operation)
                                               ↑                    ↑
                                          models.py           database.py


================================================================================
main.py
================================================================================

  PURPOSE
  -------
  The entry point of the application. FastAPI starts here.
  It receives all incoming HTTP requests, applies middleware, and hands work
  off to the appropriate route function. It also triggers the database table
  creation on startup.

  COMMUNICATES WITH
  -----------------
  → database.py  : imports Base + engine to create the table on startup;
                   uses get_db() as a dependency on every route that needs the db
  → models.py    : imports TaskCreate and TaskResponse to validate request/response data
  → crud.py      : imports and calls CRUD functions to do the actual database work

  -----------------------------------------------------------------------

  from fastapi import FastAPI, Depends, HTTPException

    FastAPI    → the core framework
    Depends    → FastAPI's dependency injection system (used to inject db sessions)
    HTTPException → lets you return proper HTTP error responses (e.g. 404 Not Found)

  -----------------------------------------------------------------------

  from fastapi.middleware.cors import CORSMiddleware

    Imports the CORS middleware bundled with FastAPI. No separate install needed.

  -----------------------------------------------------------------------

  from sqlalchemy.orm import Session

    Imports the Session type for use in route function signatures.
    Tells Python what kind of object db is.

  -----------------------------------------------------------------------

  from typing import List

    Allows you to annotate a return type as a list (e.g. List[TaskResponse]).

  -----------------------------------------------------------------------

  from . import database, crud
  from .models import TaskCreate, TaskResponse

    Imports from sibling files within the app/ package.
    The dot (.) means "from the current package" — required because app/ is a
    Python package (has __init__.py) and is run from the backend/ directory.

  -----------------------------------------------------------------------

  database.Base.metadata.create_all(bind=database.engine)

    Runs once when the server starts. Looks at all table definitions that
    inherit from Base (i.e. TaskDB) and creates them in the database if they
    don't already exist. This is how tasks.db gets its table structure on
    first run — you never need to run SQL manually.

  -----------------------------------------------------------------------

  app = FastAPI()

    Creates the application instance. Every route, middleware, and setting
    attaches to this object.

  -----------------------------------------------------------------------

  app.add_middleware(
      CORSMiddleware,
      allow_origins=["http://localhost:4200"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )

    Registers CORS as a layer that runs on every request before FastAPI handles it.
    Without this, browsers block requests from a different origin.

    allow_origins      → only this address (Angular's dev server) is permitted to call the API.
    allow_credentials  → allows cookies and auth headers cross-origin.
    allow_methods /
    allow_headers      → "*" means any HTTP method and header are permitted from allowed origins.

  -----------------------------------------------------------------------

  @app.get("/")
  def root():
      return {"status": "ok", "message": "Backend running"}

    The root endpoint. A health-check — confirms the server is alive.

  -----------------------------------------------------------------------

  @app.get("/tasks", response_model=List[TaskResponse])
  def read_tasks(db: Session = Depends(database.get_db)):
      return crud.get_tasks(db)

    Returns all tasks from the database as a list.
    response_model=List[TaskResponse] tells FastAPI to format each item using
    TaskResponse and strip anything not in that model.
    Depends(database.get_db) → FastAPI automatically opens a db session and
    passes it in. You don't call get_db() yourself.

  -----------------------------------------------------------------------

  @app.post("/tasks", response_model=TaskResponse)
  def create_task(task: TaskCreate, db: Session = Depends(database.get_db)):
      return crud.create_task(db, task)

    Creates a new task. FastAPI validates the request body against TaskCreate
    automatically — if the body is wrong, it rejects it before this runs.

  -----------------------------------------------------------------------

  @app.put("/tasks/{task_id}", response_model=TaskResponse)
  def update_task(task_id: int, completed: bool, db: Session = Depends(database.get_db)):
      task = crud.update_task(db, task_id, completed)
      if task is None:
          raise HTTPException(status_code=404, detail="Task not found")
      return task

    Updates the completed status of a task.
    {task_id} is a path parameter — FastAPI extracts the integer from the URL.
    If no task with that id exists, returns a 404 error response.

  -----------------------------------------------------------------------

  @app.delete("/tasks/{task_id}", response_model=TaskResponse)
  def delete_task(task_id: int, db: Session = Depends(database.get_db)):
      task = crud.delete_task(db, task_id)
      if task is None:
          raise HTTPException(status_code=404, detail="Task not found")
      return task

    Deletes a task by id. Returns the deleted task as confirmation.
    Returns 404 if the id doesn't exist.


================================================================================
models.py
================================================================================

  PURPOSE
  -------
  Defines the shape of data that flows IN and OUT of the API using Pydantic.
  These are not database tables — they describe the API interface only.
  FastAPI uses these to automatically validate requests and format responses.

  COMMUNICATES WITH
  -----------------
  → used by main.py   : to validate incoming request bodies and format outgoing responses
  → used by crud.py   : TaskCreate is used as the input type for create_task()
  → database.py       : TaskResponse uses Config.from_attributes to read SQLAlchemy objects

  -----------------------------------------------------------------------

  from pydantic import BaseModel

    Imports Pydantic's base class. Any class that inherits from it gets
    automatic validation — wrong types are rejected before your code runs.

  -----------------------------------------------------------------------

  from typing import Optional

    Allows fields to be marked as optional (value or nothing).

  -----------------------------------------------------------------------

  class TaskCreate(BaseModel):
      title: str
      description: Optional[str] = None

    What the API expects to RECEIVE when creating a task.
    title is required. description is optional — defaults to None if omitted.
    No id or completed — those are set by the database, not by the user.

  -----------------------------------------------------------------------

  class TaskResponse(BaseModel):
      id: int
      title: str
      description: Optional[str] = None
      completed: bool

    What the API sends BACK after creating or fetching a task.
    Includes id (assigned by the database) and completed (True/False).

  -----------------------------------------------------------------------

      class Config:
          from_attributes = True

    Tells Pydantic it can read data directly from SQLAlchemy objects (TaskDB),
    not just plain dictionaries. Required when converting a database row
    into an API response.


================================================================================
database.py
================================================================================

  PURPOSE
  -------
  Sets up the connection to the SQLite database and defines the actual
  database table using SQLAlchemy. This is the only file that defines
  what the database looks like.

  COMMUNICATES WITH
  -----------------
  → used by main.py  : imports Base + engine to create the table on startup;
                       imports get_db() as a dependency on every route that needs the database
  → used by crud.py  : imports TaskDB (the table definition) to run queries against

  -----------------------------------------------------------------------

  from sqlalchemy import create_engine, Column, Integer, String, Boolean

    create_engine  → opens the database connection
    Column         → defines a column in a table
    Integer/String/Boolean → the data types for those columns

  -----------------------------------------------------------------------

  from sqlalchemy.ext.declarative import declarative_base

    Imports the base class that all table definitions inherit from.

  -----------------------------------------------------------------------

  from sqlalchemy.orm import sessionmaker

    Imports the session factory — sessions are how you open/close
    a connection to the database for each request.

  -----------------------------------------------------------------------

  DATABASE_URL = "sqlite:///./tasks.db"

    Tells SQLAlchemy where the database file lives.
    ./ means it's created in whichever folder the server is run from (backend/).
    The file (tasks.db) is created automatically on first run.

  -----------------------------------------------------------------------

  engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

    Opens the actual connection to the database.
    check_same_thread: False is required for SQLite to work with FastAPI —
    without it, SQLite throws threading errors.

  -----------------------------------------------------------------------

  SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    A session factory. Each API request opens its own session through this.
    autocommit=False means changes aren't saved until explicitly committed —
    gives you control and prevents partial writes.

  -----------------------------------------------------------------------

  Base = declarative_base()

    The foundation class for all table definitions.
    Any class that inherits from Base gets mapped to a real database table.

  -----------------------------------------------------------------------

  class TaskDB(Base):
      __tablename__ = "tasks"

      id          = Column(Integer, primary_key=True, index=True)
      title       = Column(String, nullable=False)
      description = Column(String, nullable=True)
      completed   = Column(Boolean, default=False)

    Defines the tasks table in the database. Each Column is a table column.

    id           → auto-incrementing unique identifier. SQLite manages this automatically.
    title        → must always have a value (nullable=False).
    description  → can be empty (nullable=True).
    completed    → True/False, defaults to False when a task is first created.

    Note: TaskDB is separate from TaskCreate/TaskResponse in models.py on purpose.
    TaskDB = database shape. TaskCreate/TaskResponse = API shape. Different jobs.

  -----------------------------------------------------------------------

  def get_db():
      db = SessionLocal()
      try:
          yield db
      finally:
          db.close()

    A dependency function FastAPI calls automatically on any route that needs
    a database session. The yield hands the open session to the route function.
    The finally block ensures the session is always closed cleanly afterwards,
    even if something goes wrong mid-request.


================================================================================
crud.py
================================================================================

  PURPOSE
  -------
  Contains all the database logic: create, read, update, and delete tasks.
  This file knows nothing about HTTP — it only talks to the database.
  main.py calls these functions and handles the HTTP layer separately.
  Keeping them apart makes each file easier to understand and change.

  COMMUNICATES WITH
  -----------------
  → called by main.py   : routes in main.py call these functions to do database work
  → imports database.py : uses TaskDB (the table definition) to query the tasks table
  → imports models.py   : uses TaskCreate as the input type for create_task()

  -----------------------------------------------------------------------

  from sqlalchemy.orm import Session

    Imports the Session type for use in function signatures.
    Tells Python (and your editor) what kind of object db is.

  -----------------------------------------------------------------------

  from database import TaskDB

    Imports the TaskDB table definition so the functions can query it.

  -----------------------------------------------------------------------

  from models import TaskCreate

    Imports the TaskCreate Pydantic model so create_task() knows
    what shape of data to expect.

  -----------------------------------------------------------------------

  def get_tasks(db: Session):
      return db.query(TaskDB).all()

    Fetches every row in the tasks table and returns them as a list.
    db.query(TaskDB) = "look at the tasks table"
    .all()           = "return every row"

  -----------------------------------------------------------------------

  def get_task(db: Session, task_id: int):
      return db.query(TaskDB).filter(TaskDB.id == task_id).first()

    Fetches a single task by its id.
    .filter() is the equivalent of SQL WHERE.
    .first() returns the first match, or None if nothing is found.

  -----------------------------------------------------------------------

  def create_task(db: Session, task: TaskCreate):
      db_task = TaskDB(title=task.title, description=task.description)
      db.add(db_task)
      db.commit()
      db.refresh(db_task)
      return db_task

    Creates a new row in the tasks table.
    db_task = TaskDB(...)  → builds the new object in memory
    db.add()               → stages it (tells the session about it)
    db.commit()            → saves it permanently to the database
    db.refresh()           → re-reads it from the database so the auto-assigned id is populated
    Returns the saved task (with its new id).

  -----------------------------------------------------------------------

  def update_task(db: Session, task_id: int, completed: bool):
      db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
      if db_task:
          db_task.completed = completed
          db.commit()
          db.refresh(db_task)
      return db_task

    Finds a task by id and updates its completed field.
    The if db_task check prevents an error if the id doesn't exist.
    Returns the updated task, or None if not found.

  -----------------------------------------------------------------------

  def delete_task(db: Session, task_id: int):
      db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
      if db_task:
          db.delete(db_task)
          db.commit()
      return db_task

    Finds a task by id and removes it from the database.
    Returns the deleted task so the caller can confirm what was removed.
    Returns None if the id didn't exist.


================================================================================
END OF DOCUMENT
================================================================================

More files will be added here as the backend grows.
