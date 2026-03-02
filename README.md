# Productivity App – Environment & Setup Reference

> This README reflects the current, verified state of the project as of March 2026.
> It is the operational source of truth for running and restoring the project.

---

## 1. Project Overview

Project name: productivity-app

Purpose:
A full-stack productivity application built to:
- Learn modern backend development with FastAPI (Python)
- Learn frontend development with Angular
- Understand real-world full-stack architecture
- Build AI features using the Claude API (Anthropic)

Project root:

~/Projects/dev/productivity-app

Current folder structure:

productivity-app/
├── backend/
│   └── app/
│       ├── __init__.py      # Marks app/ as a Python package
│       ├── main.py          # FastAPI app, CORS, all API routes
│       ├── models.py        # Pydantic schemas (TaskCreate, TaskDescriptionUpdate, TaskResponse, SuggestRequest)
│       ├── database.py      # SQLite connection, SQLAlchemy table definition
│       ├── crud.py          # Database logic (Create, Read, Update, Delete, UpdateDescription)
│       └── .env             # ANTHROPIC_API_KEY — not committed to git
├── frontend/
│   └── src/
│       └── app/
│           ├── app.ts               # Routing shell — just RouterOutlet
│           ├── app.html             # Just <router-outlet />
│           ├── app.config.ts        # Angular app config — providers (HttpClient, Router)
│           ├── app.routes.ts        # Route definitions (/ and /tasks/:id lazy loaded)
│           ├── task.service.ts      # Angular service — all HTTP calls to FastAPI
│           ├── task-list/
│           │   ├── task-list.ts     # Task list component — all CRUD logic
│           │   ├── task-list.html   # Task list template — titles link to detail view
│           │   └── task-list.css    # Task list styles
│           └── task-detail/
│               ├── task-detail.ts   # Task detail component — loads task, saves description
│               ├── task-detail.html # Detail template — title, status, editable description
│               └── task-detail.css  # Task detail styles
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
- anthropic (Claude API SDK)
- python-dotenv (reads .env file at startup)

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
- backend/app/models.py    — Pydantic schemas: TaskCreate, TaskDescriptionUpdate, TaskResponse
- backend/app/database.py  — SQLite setup via SQLAlchemy, TaskDB table, get_db() session dependency
- backend/app/crud.py      — get_tasks, get_task, create_task, update_task, delete_task, update_description
- backend/app/__init__.py  — empty file that marks app/ as a Python package
- backend/.env             — stores ANTHROPIC_API_KEY (not in git, never commit this)

Database file (auto-created on first run):
- backend/tasks.db

API endpoints:
- GET    /                        → health check
- GET    /tasks                   → return all tasks
- GET    /tasks/{id}              → return single task by ID
- POST   /tasks                   → create a new task
- PUT    /tasks/{id}              → update completed status
- PATCH  /tasks/{id}              → update task description
- DELETE /tasks/{id}              → delete a task
- POST   /tasks/{id}/questions    → Claude generates 2 clarifying questions for the task
- POST   /tasks/{id}/suggest      → Claude generates context-aware content (email draft, steps, or description)

Run backend:

cd ~/Projects/dev/productivity-app/backend
uvicorn app.main:app --reload

Verify:

http://127.0.0.1:8000
http://127.0.0.1:8000/docs

AI notes:
- Model used: claude-haiku-4-5-20251001 (fast, low cost)
- API key stored in backend/.env — loaded at startup via python-dotenv
- Questions endpoint strips numbering from Claude's response before returning
- Suggest endpoint detects task type and responds with a draft, steps, or description

Status:
Backend fully working and verified via Swagger. AI endpoints tested and working.

---

## 5. Frontend (Angular)

Node management:
- nvm 0.39.7

Node:
- Version: 20.20.0 (LTS)
- npm: 10.8.2

Angular CLI:
- Version: 21.1.4 (global)

Angular project initialised with:

ng new productivity-app --directory frontend

### Frontend Application

Phases 2–4 complete. The frontend is a working Angular app with routing, task list, and task detail view.

Files:
- frontend/src/app/app.ts                    — Routing shell. Contains only RouterOutlet.
- frontend/src/app/app.html                  — Just <router-outlet />.
- frontend/src/app/app.config.ts             — Registers provideHttpClient() and provideRouter().
- frontend/src/app/app.routes.ts             — Routes: / → TaskListComponent, /tasks/:id → TaskDetailComponent (lazy loaded).
- frontend/src/app/task.service.ts           — Service layer. All HTTP calls to the backend API.
- frontend/src/app/task-list/task-list.ts    — Task list component. All CRUD logic with Angular signals.
- frontend/src/app/task-list/task-list.html  — Task list template. Task titles are links to detail view.
- frontend/src/app/task-list/task-list.css   — Task list styles.
- frontend/src/app/task-detail/task-detail.ts   — Detail component. Loads task by ID, saves description.
- frontend/src/app/task-detail/task-detail.html — Detail template. Title, status, editable description textarea.
- frontend/src/app/task-detail/task-detail.css  — Detail view styles.

Key implementation notes:
- Uses Angular signals (signal<Task[]>, signal<Task | null>) for reactive state
- App component is a pure routing shell — all logic lives in feature components
- TaskDetailComponent uses lazy loading (loadComponent with dynamic import())
- Description textarea uses [ngModel]="description()" (ngModelChange)="description.set($event)" for signal compatibility
- Clicking a task title navigates to /tasks/:id — Angular Router reads the ID via ActivatedRoute
- Textarea auto-resizes with content using ViewChild + scrollHeight — deferred with setTimeout to wait for Angular to render
- AI flow is two-step: "Generate with AI" fetches questions → user answers → "Generate Description" sends answers to Claude
- app.css is intentionally empty — all styles live in task-list.css and task-detail.css

Run frontend:

cd ~/Projects/dev/productivity-app/frontend
ng serve

Verify:

http://localhost:4200

Status:
Frontend fully working. Full CRUD verified from the browser.

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

Two servers need to run simultaneously — open two terminal tabs.

Tab 1 — Backend:

conda activate productivity_app1
cd ~/Projects/dev/productivity-app/backend
uvicorn app.main:app --reload

Tab 2 — Frontend:

cd ~/Projects/dev/productivity-app/frontend
ng serve

Then open:

http://localhost:4200

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
✅ Angular project initialised
✅ Angular service created (HttpClient, all CRUD methods)
✅ Frontend ↔ backend integration working
✅ Task list displays on page load
✅ Add task via browser form
✅ Mark task complete via checkbox
✅ Delete task via button
✅ Basic UI styling applied (layout, colours, hover states, strikethrough for done tasks)
✅ Angular routing implemented (app split into routing shell + feature components)
✅ Task detail view — click task title to navigate to /tasks/:id
✅ Task detail lazy loaded (separate JS chunk, only loads when needed)
✅ Editable task description — textarea with Save button, persists to SQLite
✅ GET /tasks/{id} and PATCH /tasks/{id} backend endpoints added
✅ Claude API integrated (anthropic + python-dotenv installed, .env configured)
✅ POST /tasks/{id}/questions — Claude returns 2 clarifying questions
✅ POST /tasks/{id}/suggest — Claude returns context-aware content (email draft, steps, or description)
✅ Two-step AI flow in Angular: Generate with AI → answer questions → Generate Description
✅ Textarea auto-resizes with content (ViewChild + scrollHeight)
✅ Duplicate styles removed from app.css (all styles now in feature component CSS files)
🟡 Next: Phase 5 — Professional Hardening
   - Error handling (user-facing messages when API calls fail)
   - Logging strategy
   - Authentication
   - Production configuration
   - Deployment

================================================================================
  END OF DOCUMENT
================================================================================