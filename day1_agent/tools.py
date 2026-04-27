import os
import re
import google.generativeai as genai

# Configure Gemini API from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def read_file(path: str) -> str:
    """Reads full PHP file content."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file {path}: {e}"

def find_undocumented(code: str) -> list[str]:
    """Finds PHP functions missing a proper docblock immediately above."""
    results = []
    lines = code.split('\n')
    for i, line in enumerate(lines):
        # Match public, private, or protected functions
        match = re.search(r'(?:public|private|protected)\s+function\s+([a-zA-Z0-9_]+)\s*\(', line)
        if match:
            fn_name = match.group(1)
            # Find the first non-blank line above the function
            prev_line_idx = i - 1
            is_documented = False
            while prev_line_idx >= 0:
                prev_line = lines[prev_line_idx].strip()
                if not prev_line:
                    prev_line_idx -= 1
                    continue
                if prev_line == '*/':
                    is_documented = True
                break
                
            if not is_documented:
                results.append(fn_name)
    return results

def generate_docblock(function_source: str) -> str:
    """Uses Gemini AI to generate a proper PHPDoc block for the given function."""
    # If no API key, fall back to local engine
    if not GEMINI_API_KEY:
        return _local_generate_docblock(function_source)
    
    try:
        # Create the prompt for Gemini
        prompt = f"""Generate a proper PHPDoc block for the following PHP function. 
Only output the docblock, nothing else. Use the standard PHPDoc format with @param and @return tags.

PHP Function:
```php
{function_source}
```

Docblock:"""

        # Call Gemini API
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        
        # Clean up the response - extract just the docblock
        docblock = response.text.strip()
        
        # Ensure it starts with /** and ends with */
        if not docblock.startswith('/**'):
            docblock = "/**\n * " + docblock
        if not docblock.endswith('*/'):
            docblock = docblock + "\n */"
            
        return docblock
        
    except Exception as e:
        print(f"Gemini API error: {e}")
        # Fall back to local engine on error
        return _local_generate_docblock(function_source)

def _local_generate_docblock(function_source: str) -> str:
    """Local fallback engine to generate a docblock given one function's source."""
    match = re.search(r'function\s+([a-zA-Z0-9_]+)\s*\((.*?)\)', function_source)
    if not match:
        name = "function"
        params_str = ""
    else:
        name = match.group(1)
        params_str = match.group(2)
        
    doc = ["/**", f" * Executes the {name} logic.", " *"]
    has_params = False
    
    if params_str.strip():
        params = params_str.split(',')
        for p in params:
            p = p.strip()
            # Extract variables (e.g. $id)
            var_match = re.search(r'(\$[a-zA-Z0-9_]+)', p)
            if var_match:
                doc.append(f" * @param mixed {var_match.group(1)}")
                has_params = True
                
    if has_params:
        doc.append(" *")
    doc.append(" * @return mixed")
    doc.append(" */")
    
    return "\n".join(doc)

def write_file(path: str, code: str) -> bool:
    """Writes updated code to disk."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(code)
        return True
    except Exception as e:
        print(f"Write error: {e}")
        return False
