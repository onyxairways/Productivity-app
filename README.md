# Productivity App – Environment & Setup Reference

> This README reflects the current, verified state of the project as of February 2026.
> It is the operational source of truth for running and restoring the project.

---

## 1. Project Overview

Project name: productivity-app

Purpose:
A full-stack productivity application built to:
- Learn modern backend development with FastAPI (Python)
- Learn frontend development with Angular
- Understand real-world full-stack architecture
- Add AI features later once the core stack is stable

Project root:

~/Projects/dev/productivity-app

Current folder structure:

productivity-app/
├── backend/
│   └── app/
│       ├── __init__.py      # Marks app/ as a Python package
│       ├── main.py          # FastAPI app, CORS, all API routes
│       ├── models.py        # Pydantic schemas (API data shapes)
│       ├── database.py      # SQLite connection, SQLAlchemy table definition
│       └── crud.py          # Database logic (Create, Read, Update, Delete)
├── frontend/                # Empty (Angular not initialised yet)
├── Miscellaneous/
│   └── backend-code-reference.md  # Plain-language code explanation
├── environment.yml          # Portable Conda snapshot
├── environment.lock.yml     # Exact Conda build snapshot
├── requirements.txt         # pip freeze output
├── project-journey.txt      # Detailed learning log
├── README.md
└── claude-project-context.txt

---

## 2. System & Tooling

OS:
- macOS (Apple Silicon / arm64)

Terminal:
- iTerm2
- Shell: zsh

Editor:
- VS Code
- `code` CLI available

### VS Code Python Extension (Required)

Install the official Microsoft Python extension.

After installation:

1. Open Command Palette (Cmd + Shift + P)
2. Run: Python: Select Interpreter
3. Select: productivity_app1 (3.11.14)

Verify the bottom status bar shows:
Python 3.11.14 (productivity_app1)

---

## 3. Backend (Python / FastAPI)

Environment Management:
- Tool: Miniconda
- Install location: ~/miniconda3
- Conda env name: productivity_app1
- Python version: 3.11.14

Base auto-activation:
- Disabled (intentional best practice)

Activate every session:

conda activate productivity_app1

Verify:

python --version

---

### Installed Backend Packages

Core stack:
- fastapi 0.129.0
- uvicorn 0.41.0
- sqlalchemy (installed during Phase 1)

Additional dependencies installed automatically:
- starlette
- pydantic
- anyio
- click
- h11
- typing-extensions
- typing-inspection
- annotated-types
- annotated-doc
- idna

All versions are captured in:
- environment.yml
- environment.lock.yml
- requirements.txt

---

## 4. Backend Application

Phase 1 complete. The backend is a fully functional REST API with persistent SQLite storage.

Files:
- backend/app/main.py      — FastAPI app, CORS middleware, all API routes
- backend/app/models.py    — Pydantic schemas: TaskCreate (input), TaskResponse (output)
- backend/app/database.py  — SQLite setup via SQLAlchemy, TaskDB table, get_db() session dependency
- backend/app/crud.py      — get_tasks, get_task, create_task, update_task, delete_task
- backend/app/__init__.py  — empty file that marks app/ as a Python package

Database file (auto-created on first run):
- backend/tasks.db

API endpoints:
- GET    /           → health check
- GET    /tasks      → return all tasks
- POST   /tasks      → create a new task
- PUT    /tasks/{id} → update completed status
- DELETE /tasks/{id} → delete a task

Run backend:

cd ~/Projects/dev/productivity-app/backend
uvicorn app.main:app --reload

Verify:

http://127.0.0.1:8000
http://127.0.0.1:8000/docs

Status:
Backend fully working and verified via Swagger.

---

## 5. Frontend Tooling (Not Yet Initialised)

Node management:
- nvm 0.39.7

Node:
- Version: 20.20.0 (LTS)
- npm: 10.8.2

Angular CLI:
- Version: 21.1.4 (global)

Frontend folder:
- Currently empty by design
- Angular project not yet created

---

## 6. Environment Reproduction & Recovery

Recreate environment (portable):

conda env create -f environment.yml
conda activate productivity_app1

Exact snapshot restore (machine-identical build):

conda env create -f environment.lock.yml

Reinstall pip packages if needed:

pip install -r requirements.txt

Update snapshots (if dependencies change):

conda env export --no-builds > environment.yml
conda env export > environment.lock.yml
python -m pip freeze > requirements.txt

---

## 7. Returning After a Break

Run:

conda activate productivity_app1
cd ~/Projects/dev/productivity-app/backend
uvicorn app.main:app --reload

Then open:

http://127.0.0.1:8000

No reinstall required.

---

## 8. Current Project Position

✅ Environment setup complete
✅ Backend working and verified
✅ Environment fully version-locked
✅ CORS middleware added
✅ Pydantic data models defined
✅ SQLite database connected (SQLAlchemy)
✅ Full CRUD API built and verified via Swagger
🟡 Angular not yet initialised
❌ Frontend ↔ backend integration not started

================================================================================
  END OF DOCUMENT
================================================================================