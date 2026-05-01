from typing import List, Any
from tools import TOOL_REGISTRY
from planner import Plan, PlanStep

def execute_plan(plan: Plan) -> List[Any]:
    """
    Executes the steps in the plan sequentially.
    This component NEVER decides the plan. It only follows instructions.
    """
    results = []
    
    print("\n--- Starting Execution ---")
    
    for step_data in plan.steps:
        print(f"\nStep {step_data.step}: {step_data.action}")
        
        tool_name = step_data.tool
        params = step_data.params
        
        if tool_name not in TOOL_REGISTRY:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        # Execute the tool
        tool_func = TOOL_REGISTRY[tool_name]
        result = tool_func(**params)
        
        print(f"Result: {result}")
        results.append(result)
        
    print("\n--- Execution Complete ---")
    return results
