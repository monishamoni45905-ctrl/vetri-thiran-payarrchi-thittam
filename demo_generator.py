from textwrap import dedent

def generate_demo_workout(goal, intensity):
    return dedent(f"""
    7-DAY FITBUDDY DEMO WORKOUT PLAN
    Goal: {goal}
    Intensity: {intensity.title()}

    Important: This is a local demo response. Connect GEMINI_API_KEY for real AI generation.

    DAY 1 – Full Body Foundation
    Warm-up: 5–10 minutes of easy walking and mobility.
    Main workout:
    - Bodyweight squats: 3 sets × 10 reps
    - Wall or incline push-ups: 3 × 8
    - Glute bridges: 3 × 12
    - Bird-dog: 2 × 8 each side
    Cool-down: 5 minutes of gentle stretching.

    DAY 2 – Cardio + Core
    Warm-up: 5–10 minutes.
    Main workout:
    - Brisk walk: 15–25 minutes
    - Dead bug: 2 × 8 each side
    - Standing knee raises: 2 × 10 each side
    Cool-down: 5 minutes.

    DAY 3 – Lower Body
    Warm-up: 5–10 minutes.
    Main workout:
    - Sit-to-stand: 3 × 10
    - Reverse lunges or supported split squats: 2 × 8 each side
    - Calf raises: 3 × 12
    Cool-down: 5 minutes.

    DAY 4 – Recovery / Mobility
    15–20 minutes of comfortable mobility, light walking, and stretching.

    DAY 5 – Upper Body + Core
    Warm-up: 5–10 minutes.
    Main workout:
    - Incline push-ups: 3 × 8
    - Backpack rows: 3 × 10
    - Shoulder taps: 2 × 8 each side
    - Front plank from knees or toes: 3 × 15–30 seconds
    Cool-down: 5 minutes.

    DAY 6 – Full Body Circuit
    Complete 2–3 comfortable rounds:
    - Squats: 10
    - Incline push-ups: 8
    - Glute bridges: 12
    - March in place: 45 seconds
    Rest as needed between exercises.

    DAY 7 – Active Recovery
    Easy walking for 15–30 minutes plus gentle stretching.

    SAFETY
    Stop if an exercise causes pain, dizziness, or unusual symptoms. For medical conditions,
    injuries, or concerns, get guidance from a qualified professional.
    """).strip()

def generate_demo_tip(goal):
    return (
        f"For a goal of {goal.strip()}, build meals around regular balanced foods, "
        "include a source of protein and fibre, drink enough water, and avoid skipping meals. "
        "Adjust food choices to your individual needs and seek professional nutrition advice "
        "for medical or dietary conditions."
    )

def update_demo_plan(original, feedback):
    return (
        original + "\n\nFEEDBACK-BASED UPDATE (DEMO)\n"
        + f"User feedback: {feedback.strip()}\n"
        + "Adjustment: Keep the existing structure, reduce or increase difficulty according "
          "to comfort, and add recovery time where requested. Connect Gemini for a true AI revision."
    )
