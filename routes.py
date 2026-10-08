import os
from datetime import datetime
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .database import get_db
from .models import User, WorkoutPlan
from .schemas import FeedbackRequest, UserInput, WorkoutRequest
from .services.gemini_service import get_gemini_service

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
router = APIRouter()

def save_user(db, data):
    user = db.query(User).filter(User.user_id == data.user_id).first()
    if user:
        user.name, user.age, user.weight = data.name, data.age, data.weight
        user.goal, user.intensity = data.goal, data.intensity
    else:
        user = User(user_id=data.user_id, name=data.name, age=data.age, weight=data.weight,
                    goal=data.goal, intensity=data.intensity)
        db.add(user)
    db.commit()
    db.refresh(user)
    return user

def save_plan(db, user_id, plan, tip):
    workout = WorkoutPlan(user_id=user_id, original_plan=plan, nutrition_tip=tip)
    db.add(workout)
    db.commit()
    db.refresh(workout)
    return workout

def get_current_plan(db, user_id):
    return db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).order_by(WorkoutPlan.id.desc()).first()

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html",
                                      context={"title": "FitBuddy - AI Fitness Plan Generator"})

@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout_html(request: Request, user_id: int = Form(...), name: str = Form(...),
                          age: int = Form(...), weight: float = Form(...), goal: str = Form(...),
                          intensity: str = Form(...), db: Session = Depends(get_db)):
    form = {"user_id": user_id, "name": name, "age": age, "weight": weight,
            "goal": goal, "intensity": intensity}
    try:
        data = UserInput(**form)
        user = save_user(db, data)
        service = get_gemini_service()
        plan = service.workout_plan(user.name, user.age, user.weight, user.goal, user.intensity)
        tip = service.nutrition_tip(user.goal)
        workout = save_plan(db, user.user_id, plan, tip)
        return templates.TemplateResponse(request=request, name="result.html", context={
            "title": "Your Personalized Workout Plan", "user": user, "workout": workout,
            "using_gemini": service.using_real_gemini})
    except Exception as exc:
        return templates.TemplateResponse(request=request, name="index.html", context={
            "title": "FitBuddy - AI Fitness Plan Generator", "error": str(exc), "form": form}, status_code=500)

@router.get("/feedback/{user_id}", response_class=HTMLResponse)
def feedback_page(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    workout = get_current_plan(db, user_id)
    if not user or not workout:
        raise HTTPException(404, "User or workout plan not found.")
    return templates.TemplateResponse(request=request, name="feedback.html",
                                      context={"title": "Update Your Plan", "user": user, "workout": workout})

@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(request: Request, user_id: int = Form(...), feedback: str = Form(...),
                    db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    workout = get_current_plan(db, user_id)
    if not user or not workout:
        raise HTTPException(404, "User or workout plan not found.")
    try:
        service = get_gemini_service()
        revised = service.update_plan(workout.original_plan, feedback, user.goal, user.intensity)
        workout.updated_plan, workout.feedback, workout.updated_at = revised, feedback.strip(), datetime.utcnow()
        db.commit()
        db.refresh(workout)
        return templates.TemplateResponse(request=request, name="result.html", context={
            "title": "Updated Workout Plan", "user": user, "workout": workout,
            "message": "Your plan has been updated based on your feedback.",
            "using_gemini": service.using_real_gemini})
    except Exception as exc:
        return templates.TemplateResponse(request=request, name="feedback.html", context={
            "title": "Update Your Plan", "user": user, "workout": workout, "error": str(exc)}, status_code=500)

@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.id.desc()).all()
    rows = [{"user": user, "plan": get_current_plan(db, user.user_id)} for user in users]
    return templates.TemplateResponse(request=request, name="all_users.html",
                                      context={"title": "All Users & Workout Plans", "rows": rows})

@router.get("/api/generate-workout")
def api_generate_workout(request_data: WorkoutRequest):
    service = get_gemini_service()
    result = service.workout_plan("API User", 18, 60, request_data.goal, request_data.intensity)
    return {"model": service.plan_model, "workout_plan": result, "demo_mode": not service.using_real_gemini}

@router.post("/api/generate-plan")
def api_generate_plan(data: UserInput, db: Session = Depends(get_db)):
    try:
        user = save_user(db, data)
        service = get_gemini_service()
        plan = service.workout_plan(user.name, user.age, user.weight, user.goal, user.intensity)
        tip = service.nutrition_tip(user.goal)
        workout = save_plan(db, user.user_id, plan, tip)
        return {"message": "Workout plan generated and saved successfully.", "user_id": user.user_id,
                "workout_plan": workout.original_plan, "nutrition_tip": workout.nutrition_tip,
                "demo_mode": not service.using_real_gemini}
    except Exception as exc:
        raise HTTPException(500, str(exc)) from exc

@router.get("/api/nutrition-tip")
def api_nutrition_tip(goal: str):
    service = get_gemini_service()
    try:
        return {"goal": goal, "nutrition_tip": service.nutrition_tip(goal),
                "demo_mode": not service.using_real_gemini}
    except Exception as exc:
        raise HTTPException(500, str(exc)) from exc

@router.post("/api/update-plan/{user_id}")
def api_update_plan(user_id: int, data: FeedbackRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    workout = get_current_plan(db, user_id)
    if not user or not workout:
        raise HTTPException(404, "User or workout plan not found.")
    service = get_gemini_service()
    try:
        revised = service.update_plan(workout.original_plan, data.feedback, user.goal, user.intensity)
        workout.updated_plan, workout.feedback, workout.updated_at = revised, data.feedback.strip(), datetime.utcnow()
        db.commit()
        return {"user_id": user_id, "updated_plan": revised, "demo_mode": not service.using_real_gemini}
    except Exception as exc:
        raise HTTPException(500, str(exc)) from exc

@router.get("/api/users")
def api_users(db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.id.desc()).all()
    return [{"user_id": u.user_id, "name": u.name, "age": u.age, "weight": u.weight,
             "goal": u.goal, "intensity": u.intensity,
             "original_plan": (p.original_plan if p else None),
             "updated_plan": (p.updated_plan if p else None)}
            for u in users for p in [get_current_plan(db, u.user_id)]]

@router.delete("/api/users/{user_id}")
def api_delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found.")
    db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).delete(synchronize_session=False)
    db.delete(user)
    db.commit()
    return {"message": f"User {user_id} deleted successfully."}
