import sys
from planner import generate_plan
from executor import execute_plan

def main():
    print("Welcome to the Planning Agent (Track B)")
    
    # 1. Get User Request
    user_request = input("\nEnter your request (e.g., 'Search for laptops and check stock'): ")
    if not user_request:
        user_request = "Search for laptops, check inventory for the main one, and create a ticket if low stock."
        print(f"Using default request: {user_request}")

    # 2. Planner Runs
    print("\nThinking... (Generating Plan)")
    plan = generate_plan(user_request)

    # 3. Plan is Displayed
    print("\nPROPOSED PLAN:")
    for step in plan.steps:
        print(f"  Step {step.step}: {step.action}")
        print(f"    Tool: {step.tool}")
        print(f"    Params: {step.params}")

    # 4. Human Approval Step
    print("\n--- Human Approval Required ---")
    approval = input("Does this plan look correct? Type 'yes' to proceed: ").strip().lower()

    if approval != "yes":
        print("\nExecution cancelled by user.")
        sys.exit(0)

    # 5. Executor Runs the Plan
    try:
        execute_plan(plan)
        print("\nTask completed successfully!")
    except Exception as e:
        print(f"\nExecution failed: {e}")

if __name__ == "__main__":
    main()
