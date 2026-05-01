import subprocess
import time

def run_test():
    # Start the process
    process = subprocess.Popen(
        ['python', 'main.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    # 1. Send the user request
    print("--- Sending User Request ---")
    process.stdin.write("Search for laptops and check stock for the first one.\n")
    process.stdin.flush()

    # Read output until we see the plan and approval prompt
    while True:
        line = process.stdout.readline()
        if not line:
            break
        print(line, end='')
        if "Type 'yes' to proceed" in line:
            break

    # 2. Send the human approval
    print("\n--- Sending Human Approval ---")
    process.stdin.write("yes\n")
    process.stdin.flush()

    # Read the rest of the output
    for line in process.stdout:
        print(line, end='')

    # Check for errors
    stderr = process.stderr.read()
    if stderr:
        print(f"\nSTDERR: {stderr}")

if __name__ == "__main__":
    run_test()
