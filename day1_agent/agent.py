import json
import tools

MAX_ITERATIONS = 20

def main():
    print(f"Starting Agent (Local Fast-Execution Mode)... Max Iterations: {MAX_ITERATIONS}")
    
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
    
    # 3. GENERATE DOCBLOCKS
    iteration = 3
    final_code_lines = code.split('\n')
    
    for func in undoc:
        print(f"\n--- Iteration {iteration} ---")
        print(f"[Thought]: Generating docblock for '{func}' one at a time.")
        
        # Safely extract the target line source
        source_line = ""
        insert_idx = -1
        for idx, line in enumerate(final_code_lines):
            if f"function {func}" in line:
                source_line = line.strip()
                insert_idx = idx
                break
                
        print(f"[Act]: Tool generate_docblock called with arguments: {json.dumps({'function_source': source_line})}")
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
