import json
from validator import Validator

def run_test(validator: Validator, task: str, plan_steps: list, expected_valid: bool, description: str):
    plan_data = {"steps": [{"step_number": i+1, "action": step} for i, step in enumerate(plan_steps)]}
    plan_json = json.dumps(plan_data)
    
    print(f"\nTEST: {description}")
    print("-" * len(f"TEST: {description}"))
    print(f"TASK: {task}")
    print("PLAN:")
    for step in plan_steps:
        print(f"  - {step}")
    
    report = validator.validate_plan(task, plan_json)
    
    success = (report.is_valid == expected_valid)
    status = "PASS" if success else "FAIL"
    
    print(f"RESULT: {status} (Expected: {expected_valid}, Got: {report.is_valid})")
    if not report.is_valid:
        print(f"FEEDBACK: {report.feedback}")
    
    return success

def main():
    print("\n" + "="*50)
    print(" VALIDATOR TEST SUITE")
    print("="*50)
    
    validator = Validator()
    
    test_cases = [
        {
            "description": "Correct Tea Plan",
            "task": "Make a cup of tea",
            "plan": ["Boil water", "Add tea bag to cup", "Pour water into cup", "Steep for 3 minutes"],
            "expected": True
        },
        {
            "description": "Missing Critical Step (Boiling)",
            "task": "Make a cup of tea",
            "plan": ["Add tea bag to cup", "Pour cold water into cup", "Drink immediately"],
            "expected": False
        },
        {
            "description": "Wrong Logical Order",
            "task": "Make a cup of tea",
            "plan": ["Pour water into cup", "Boil water in the cup", "Add tea bag"],
            "expected": False
        },
        {
            "description": "Over-planning (Unrelated steps)",
            "task": "Make a cup of tea",
            "plan": ["Paint the kitchen", "Boil water", "Add tea bag", "Pour water"],
            "expected": False
        },
        {
            "description": "Semantic Impossibility",
            "task": "Travel to the moon this afternoon",
            "plan": ["Pack a suitcase", "Drive to the local airport", "Take a flight to the moon"],
            "expected": False
        }
    ]
    
    results = []
    for tc in test_cases:
        success = run_test(validator, tc["task"], tc["plan"], tc["expected"], tc["description"])
        results.append(success)
    
    total = len(results)
    passed = sum(results)
    print("\n" + "="*50)
    print(f" SUMMARY: {passed}/{total} tests passed.")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
