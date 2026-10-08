# FitBuddy – AI Fitness Plan Generator using Gemini

Complete FastAPI + Jinja2 + SQLite/SQLAlchemy student project based on the supplied FitBuddy report.

## Features
- User profile form: ID, name, age, weight, goal, intensity.
- Gemini-generated 7-day workout plan.
- Gemini-generated nutrition/recovery tip.
- Feedback-based revised plan.
- SQLite persistence for users and original/updated plans.
- Admin/development dashboard.
- JSON APIs + Swagger docs.
- Demo fallback mode for testing without an API key.
- Responsive frontend with no Node/npm build step.

## Current Gemini implementation
The supplied report refers to older Gemini 1.5 APIs. This implementation uses the current `google-genai` SDK and configurable model names. The defaults are `gemini-3.8-flash`; change them in `.env` if your API account exposes another model.

## VS Code setup on Windows

1. Extract/open this folder in VS Code.
2. Terminal → New Terminal.
3. Create environment:
```powershell
py -m venv .venv
```
4. Activate:
```powershell
.venv\Scripts\Activate.ps1
```
or Command Prompt:
```cmd
.venv\Scriptsctivate.bat
```
5. Install:
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```
6. Copy `.env.example` to `.env`.
7. For real Gemini AI, put your key in `GEMINI_API_KEY`.
8. Start:
```powershell
uvicorn app.main:app --reload
```
9. Open:
- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

## Test
```powershell
pytest -q
```

## Demo mode
`ALLOW_DEMO_MODE=true` lets you test the complete website/database flow without a Gemini key. It clearly labels generated output as demo content. For actual AI generation, add `GEMINI_API_KEY` and restart the server.

## API endpoints
- `GET /`
- `POST /generate-workout`
- `GET /feedback/{user_id}`
- `POST /submit-feedback`
- `GET /view-all-users`
- `POST /api/generate-plan`
- `GET /api/nutrition-tip?goal=weight%20loss`
- `POST /api/update-plan/{user_id}`
- `GET /api/users`
- `DELETE /api/users/{user_id}`
- `GET /health`

## Troubleshooting
`ModuleNotFoundError`: activate `.venv`, then `pip install -r requirements.txt`.

Gemini error: verify `GEMINI_API_KEY`, model name, and restart Uvicorn.

Port busy:
```powershell
uvicorn app.main:app --reload --port 8001
```

FitBuddy is a student wellness project, not a medical or clinical system. AI output is general information and should not replace qualified professional advice.
