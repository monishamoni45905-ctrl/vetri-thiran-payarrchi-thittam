import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .database import init_db
from .routes import router

load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI(title="FitBuddy - AI Fitness Plan Generator",
              description="AI-powered wellness plan generator using FastAPI, SQLite, and Gemini.",
              version="1.0.0")
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
app.include_router(router)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/health")
def health():
    from .services.gemini_service import get_gemini_service
    service = get_gemini_service()
    return {"status": "ok", "gemini_configured": service.using_real_gemini,
            "demo_mode": not service.using_real_gemini}
