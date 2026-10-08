import os
from pathlib import Path
os.environ["GEMINI_API_KEY"] = ""
os.environ["ALLOW_DEMO_MODE"] = "true"
os.environ["DATABASE_URL"] = "sqlite:///./test_fitbuddy.db"

from fastapi.testclient import TestClient
from app.database import Base, engine
from app.main import app

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
client = TestClient(app)

def teardown_module():
    Base.metadata.drop_all(bind=engine)
    path = Path("test_fitbuddy.db")
    if path.exists(): path.unlink()

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "FitBuddy" in response.text

def test_generate_plan():
    response = client.post("/api/generate-plan", json={
        "user_id": 9001, "name": "Test User", "age": 20, "weight": 60,
        "goal": "general fitness", "intensity": "medium"})
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 9001
    assert data["workout_plan"]
    assert data["nutrition_tip"]

def test_nutrition_tip():
    response = client.get("/api/nutrition-tip", params={"goal": "muscle gain"})
    assert response.status_code == 200
    assert response.json()["nutrition_tip"]

def test_update_plan():
    response = client.post("/api/update-plan/9001", json={"feedback": "Please include more recovery time."})
    assert response.status_code == 200
    assert response.json()["updated_plan"]

def test_users_page():
    response = client.get("/view-all-users")
    assert response.status_code == 200
    assert "Test User" in response.text

def test_delete_user():
    response = client.delete("/api/users/9001")
    assert response.status_code == 200
    assert client.get("/api/users").json() == []
