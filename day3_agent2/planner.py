import os
from typing import List
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel

load_dotenv()

class PlanStep(BaseModel):
    step_number: int
    action: str

class Plan(BaseModel):
    steps: List[PlanStep]

class Planner:
    def __init__(self, model: str = "llama-3.3-70b-versatile"):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = model
        self.system_prompt = """
You are a highly efficient Planning Agent. Your goal is to generate a minimal, logical, and atomic plan for any task provided by the user.

RULES:
1. Each step must be a single, atomic action.
2. The plan must be minimal (no unnecessary steps).
3. Nessesery substeps should be mentioned in the plan.
3. The steps must be in the correct logical order.
4. Output MUST be in JSON format matching the schema: {"steps": [{"step_number": 1, "action": "Step description"}]}.
5. Do NOT include any introductory or explanatory text. Only the JSON.
"""

    def generate_plan(self, task: str, feedback: str = None) -> Plan:
        prompt = f"Task: {task}"
        if feedback:
            prompt += f"\n\nFeedback from previous attempt:\n{feedback}\nPlease improve the plan based on this feedback."

        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            model=self.model,
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content
        return Plan.model_validate_json(content)

if __name__ == "__main__":
    planner = Planner()
    task = "Make a cup of tea"
    plan = planner.generate_plan(task)
    for step in plan.steps:
        print(f"{step.step_number}. {step.action}")
