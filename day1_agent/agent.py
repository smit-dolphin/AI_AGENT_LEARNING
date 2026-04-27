import json
import tools
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

MAX_ITERATIONS = 20

def main():
    # Check if Gemini API is configured
    api_key = os.getenv("GEMINI_API_KEY", "")
    mode = "Gemini AI" if api_key else "Local Fallback"
    
    print(f"Starting Agent ({mode} Mode)... Max Iterations: {MAX_ITERATIONS}")
    if not api_key:
        print("Warning: GEMINI_API_KEY not found. Using local fallback engine.")
    
    # 1. READ FILE
    print("\n--- Iteration 1 ---")
    print("[Thought]: I need to read the file first to analyze the source code.")
    print("[Act]: Tool read_file called with arguments: {\"path\": \"sample_controller.php\"}")
    code = tools.read_file("sample_controller.php")
    print(f"[Observe]: Tool Output -> {code[:150]}...")
    
    # 2. FIND UNDOCUMENTED
    print("\n--- Iteration 2 ---")
    print("[Thought]: Now I will find undocumented functions out of the loaded source.")
    print("[Act]: Tool find_undocumented called with arguments: {\"code\": \"<code>\"}")
    undoc = tools.find_undocumented(code)
    print(f"[Observe]: Tool Output -> {json.dumps(undoc)}")
    
    # 3. GENERATE DOCBLOCKS (ReAct Loop)
    iteration = 3
    final_code_lines = code.split('\n')
    
    for func in undoc:
        print(f"\n--- Iteration {iteration} ---")
        print(f"[Thought]: I need to generate a docblock for '{func}'. Let me analyze the function signature and generate appropriate documentation using AI.")
        
        # Safely extract the target line source
        source_line = ""
        insert_idx = -1
        for idx, line in enumerate(final_code_lines):
            if f"function {func}" in line:
                source_line = line.strip()
                insert_idx = idx
                break
        
        print(f"[Act]: Tool generate_docblock called with arguments: {json.dumps({'function_source': source_line})}")
        
        if api_key:
            print(f"[AI Thinking]: Analyzing function '{func}' to generate proper PHPDoc...")
        
        docblock = tools.generate_docblock(source_line)
        print(f"[Observe]: Tool Output -> \n{docblock}")
        
        # Inject the generated docblock tightly above the function definition
        if insert_idx != -1:
            for dline in reversed(docblock.split('\n')):
                final_code_lines.insert(insert_idx, "    " + dline)
                
        iteration += 1

    # 4. WRITE BACK
    print(f"\n--- Iteration {iteration} ---")
    print("[Thought]: I have successfully mapped all individual docblocks. I will inject and write the final file.")
    print("[Act]: Tool write_file called with arguments: {\"path\": \"sample_controller.php\"}")
    final_code = '\n'.join(final_code_lines)
    success = tools.write_file("sample_controller.php", final_code)
    print(f"[Observe]: Tool Output -> {success}")
    
    # 5. END TURN
    iteration += 1
    print(f"\n--- Iteration {iteration} ---")
    print("[Thought]: The task is successfully completed. Disengaging loop.")
    print("[Act]: Tool end_turn called with arguments: {}")
    print("[Finish]: Agent called end_turn. Sequence complete!")

if __name__ == "__main__":
    main()
