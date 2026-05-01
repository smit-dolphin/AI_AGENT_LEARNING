import sys
from planner import Planner
from validator import Validator

def display_plan(plan):
    print("\n" + "="*50)
    print(" GENERATED PLAN")
    print("="*50)
    for step in plan.steps:
        print(f" {step.step_number}. {step.action}")
    print("="*50 + "\n")

def main():
    print("\n" + "*"*60)
    print(" GENERIC PLANNER + VALIDATOR AGENT")
    print("*"*60)
    
    try:
        task = input("\nEnter the task you want to plan: ").strip()
    except EOFError:
        return
        
    if not task:
        print("\n[!] No task entered. Exiting.")
        return

    planner = Planner()
    validator = Validator()

    max_attempts = 3
    attempt = 1
    feedback = None
    final_plan = None

    while attempt <= max_attempts:
        print(f"\n>>> ATTEMPT {attempt}: Planning...")
        try:
            plan = planner.generate_plan(task, feedback)
            plan_json = plan.model_dump_json(indent=2)
            
            display_plan(plan)
            
            print(f">>> ATTEMPT {attempt}: Validating...")
            report = validator.validate_plan(task, plan_json)
            
            if report.is_valid:
                print("\n[SUCCESS] Plan is VALID!")
                final_plan = plan
                break
            else:
                print("\n[INVALID] Issues found in plan:")
                print(f"Feedback: {report.feedback}")
                feedback = report.feedback
                attempt += 1
                if attempt <= max_attempts:
                    print("-" * 30)
                    print(f"Retrying (Attempt {attempt}/{max_attempts})...")
        except Exception as e:
            print(f"\n[ERROR] Something went wrong: {e}")
            break

    if final_plan:
        print("\n" + "#"*50)
        print(" FINAL APPROVED PLAN")
        print("#"*50)
        for step in final_plan.steps:
            print(f" {step.step_number}. {step.action}")
        print("#"*50 + "\n")
    else:
        print(f"\n[FAILURE] Could not generate a valid plan after {max_attempts} attempts.")

if __name__ == "__main__":
    main()
