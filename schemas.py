from pydantic import BaseModel, Field, field_validator

class UserInput(BaseModel):
    user_id: int = Field(..., ge=1)
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=13, le=100)
    weight: float = Field(..., gt=0, le=500)
    goal: str = Field(..., min_length=2, max_length=100)
    intensity: str

    @field_validator("name", "goal")
    @classmethod
    def strip_text(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Value cannot be empty")
        return value

    @field_validator("intensity")
    @classmethod
    def valid_intensity(cls, value):
        value = value.lower().strip()
        if value not in {"low", "medium", "high"}:
            raise ValueError("Intensity must be low, medium, or high")
        return value

class WorkoutRequest(BaseModel):
    goal: str = Field(..., min_length=2, max_length=100)
    intensity: str

    @field_validator("intensity")
    @classmethod
    def valid_intensity(cls, value):
        value = value.lower().strip()
        if value not in {"low", "medium", "high"}:
            raise ValueError("Intensity must be low, medium, or high")
        return value

class FeedbackRequest(BaseModel):
    feedback: str = Field(..., min_length=3, max_length=2000)

class NutritionRequest(BaseModel):
    goal: str = Field(..., min_length=2, max_length=100)
