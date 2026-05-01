import os
import json
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from groq import Groq
from dotenv import load_dotenv

# Task 1 Answers (Architecture Verification):
# 1. Does the planner call tools? -> No. It only generates the plan.
# 2. Where do parameters (like SKU) come from? -> From the plan itself (hallucinated or extracted from context).
# 3. Should execution continue if step 1 fails? -> No (dependent steps).

load_dotenv()

class PlanStep(BaseModel):
    step: int = Field(..., description="The order number of the step")
    action: str = Field(..., description="Human-readable description of what to do")
    tool: str = Field(..., description="The name of the tool to use")
    params: Dict[str, Any] = Field(..., description="Arguments for the tool")

class Plan(BaseModel):
    steps: List[PlanStep] = Field(..., description="List of sequential steps")

def generate_plan(user_request: str) -> Plan:
    """
    Generates a structured 3-step plan based on the user request.
    This component uses Groq as the LLM engine.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("WARNING: No GROQ_API_KEY found. Using mock planner logic.")
        return Plan(steps=[
            PlanStep(step=1, action="Search for products matching 'laptop'", tool="search_products", params={"query": "laptop"}),
            PlanStep(step=2, action="Check inventory for SKU-123", tool="check_inventory", params={"sku": "SKU-123"}),
            PlanStep(step=3, action="Create high priority support ticket for low stock", tool="create_support_ticket", params={"title": "Restock Laptop Pro", "priority": "high"})
        ])

    client = Groq(api_key=api_key)
    
    prompt = f"""
    You are a Planning Agent. Your job is to create a structured 3-step plan to fulfill the user's request.
    
    User Request: "{user_request}"
    
    Available Tools:
    - search_products(query: str): Returns a list of products with SKUs.
    - check_inventory(sku: str): Returns stock status for a SKU.
    - create_support_ticket(title: str, priority: str): Creates a ticket.
    
    Guidelines:
    1. The plan must contain exactly 3 steps.
    2. Step 1 should be a search.
    3. Step 2 should check inventory (use 'SKU-123' if a specific SKU is needed for this demo).
    4. Step 3 should create a ticket.
    5. Output the plan in strict JSON format. 
    6. ONLY output the JSON, no other text.
    
    JSON Schema:
    {{
      "steps": [
        {{
          "step": 1,
          "action": "description",
          "tool": "tool_name",
          "params": {{ "param_name": "value" }}
        }}
      ]
    }}
    """

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant that outputs only JSON."},
            {"role": "user", "content": prompt}
        ],
        model="llama-3.3-70b-versatile",
        response_format={"type": "json_object"}
    )
    
    try:
        plan_data = json.loads(response.choices[0].message.content)
        return Plan(**plan_data)
    except Exception as e:
        print(f"Error parsing plan: {e}")
        print(f"Raw response: {response.choices[0].message.content}")
        raise
