import os
from functools import lru_cache
from dotenv import load_dotenv
from .demo_generator import generate_demo_tip, generate_demo_workout, update_demo_plan

load_dotenv()

try:
    from google import genai
except ImportError:
    genai = None

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.plan_model = os.getenv("GEMINI_PLAN_MODEL", "gemini-3.8-flash")
        self.tip_model = os.getenv("GEMINI_TIP_MODEL", "gemini-3.8-flash")
        self.update_model = os.getenv("GEMINI_UPDATE_MODEL", "gemini-3.8-flash")
        self.demo_mode = os.getenv("ALLOW_DEMO_MODE", "true").lower() == "true"
        self.client = genai.Client(api_key=self.api_key) if self.api_key and genai else None

    @property
    def using_real_gemini(self):
        return self.client is not None

    def _generate(self, model, prompt):
        if not self.client:
            raise RuntimeError("Gemini API is not configured.")
        response = self.client.models.generate_content(model=model, contents=prompt)
        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned an empty response.")
        return text.strip()

    def workout_plan(self, name, age, weight, goal, intensity):
        prompt = f"""
You are FitBuddy, a wellness-focused workout planning assistant.

Create a practical 7-day general fitness plan for:
Name: {name}
Age: {age}
Weight: {weight} kg
Fitness goal: {goal}
Workout intensity: {intensity}

Requirements:
- Organize clearly as Day 1 through Day 7.
- Include warm-up, main workout, and cool-down/recovery guidance.
- Give sets/repetitions or a reasonable duration.
- Include at least one recovery/low-intensity day.
- Keep it suitable for general wellness.
- Do not diagnose conditions or promise medical/weight-loss outcomes.
- Tell the user to stop if they experience pain, dizziness, or unusual symptoms.
"""
        if self.using_real_gemini:
            return self._generate(self.plan_model, prompt)
        if self.demo_mode:
            return generate_demo_workout(goal, intensity)
        raise RuntimeError("GEMINI_API_KEY is missing and demo mode is disabled.")

    def nutrition_tip(self, goal):
        prompt = f"""
Give one concise, practical nutrition or recovery tip for a general fitness goal: {goal}.
Keep it friendly and easy to understand. Focus on balanced meals, hydration, protein/fibre,
or recovery habits. Do not prescribe restrictive diets or diagnose medical conditions.
"""
        if self.using_real_gemini:
            return self._generate(self.tip_model, prompt)
        if self.demo_mode:
            return generate_demo_tip(goal)
        raise RuntimeError("GEMINI_API_KEY is missing and demo mode is disabled.")

    def update_plan(self, original_plan, feedback, goal, intensity):
        prompt = f"""
You are revising an existing general wellness workout plan.

Fitness goal: {goal}
Current intensity: {intensity}

ORIGINAL PLAN:
{original_plan}

USER FEEDBACK:
{feedback}

Return a complete revised 7-day plan, not just a list of changes.
Preserve useful structure, apply the feedback where reasonable, and keep a recovery day.
Avoid medical claims or unsafe instructions.
"""
        if self.using_real_gemini:
            return self._generate(self.update_model, prompt)
        if self.demo_mode:
            return update_demo_plan(original_plan, feedback)
        raise RuntimeError("GEMINI_API_KEY is missing and demo mode is disabled.")

@lru_cache
def get_gemini_service():
    return GeminiService()
