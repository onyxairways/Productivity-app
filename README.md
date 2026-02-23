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
│       └── main.py
├── frontend/                # Empty (Angular not initialised yet)
├── Miscellaneous/           # Empty (notes/screenshots)
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

File:
backend/app/main.py

Current contents:

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "message": "Backend running"}

Run backend:

cd ~/Projects/dev/productivity-app/backend
uvicorn app.main:app --reload

Verify:

http://127.0.0.1:8000
http://127.0.0.1:8000/docs

Status:
Backend confirmed working.

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
🟡 CORS not yet added  
🟡 Angular not yet initialised  
❌ Frontend ↔ backend integration not started  

================================================================================
  END OF DOCUMENT
================================================================================