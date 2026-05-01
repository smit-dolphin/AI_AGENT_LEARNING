import os
from typing import List, Optional
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, Field

load_dotenv()

class ValidationReport(BaseModel):
    is_valid: bool = Field(description="Whether the plan is valid")
    feedback: Optional[str] = Field(description="Feedback for the planner if the plan is invalid")

class Validator:
    def __init__(self, model: str = "llama-3.3-70b-versatile"):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = model
        self.system_prompt = """
You are a Critical Validation Agent. Your goal is to analyze a proposed plan for a specific task and determine if it is correct, minimal, and logical.

VALIDATION CRITERIA:
1. Logical Order: Are the steps in the right sequence?
2. Completeness: Are any critical steps missing?
3. substeps: Are any steps missing any necessary substeps?
3. Minimality: Are there unnecessary steps?
4. Atomic: Is each step a single action?
5. Semantic Validity: Do the steps make real-world sense for the task?

Output MUST be in JSON format matching the schema:
{
  "is_valid": boolean,
  "feedback": "Detailed feedback string highlighting specific issues, or empty if valid"
}
"""

    def validate_plan(self, task: str, plan_json: str) -> ValidationReport:
        prompt = f"Task: {task}\n\nProposed Plan:\n{plan_json}"
        
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            model=self.model,
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content
        return ValidationReport.model_validate_json(content)

if __name__ == "__main__":
    validator = Validator()
    task = "Make a cup of tea"
    plan_json = '{"steps": [{"step_number": 1, "action": "Add milk"}, {"step_number": 2, "action": "Boil water"}]}'
    report = validator.validate_plan(task, plan_json)
    print(f"Is Valid: {report.is_valid}")
    print(f"Feedback: {report.feedback}")
