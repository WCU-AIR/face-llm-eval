import re

def get_last_non_empty_line(text):
    clean_text = re.sub(r'\x1b\[[0-9;]*m', '', text) 
    lines = clean_text.splitlines()
    for line in reversed(lines):
        if line.strip():
            clean_status = line.strip().split('(')[0].strip()
            return clean_status
    return ""

# Extract passed and total test cases from Kattis feedback
def get_test_cases_info(feedback):
    matches = re.findall(r"Test cases:\s*\[.*?\]\s*(\d+)\s*/\s*(\d+)", feedback)
    if matches:
        last_match = matches[-1]
        passed = int(last_match[0])
        total = int(last_match[1])
        if passed == total: 
            return passed, total
        return passed - 1, total  
    return 0, 0

def api_call(input_text, model, client):
    prompt = (
        "You are a Python programming expert who writes clean, efficient code for competitive‐programming style problems.\n"
        "When given a problem statement and test cases, produce a single Python script that:\n"
        "1. Uses only the Python standard library (no external imports).\n"
        "2. Reads from user input and prints the output exactly as described.\n"
        "3. Chooses descriptive, non-conflicting variable and function names.\n"
        "4. Includes no additional commentary—only the code, wrapped in a single fenced code block (```python …```).\n"
        "5. Correctly handles edge cases (empty inputs, minimum/maximum values, etc.).\n"
        "6. Does not hard-code any test-specific values (your solution must generalize).\n"
        "7. Make sure to print the result!\n"
        "Below is the full problem. Write only the Python code.\n\n"
        + input_text
    )

    response = client.chat(
        model=model, 
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response["message"]["content"]

# Convert Ollama output to just Python code
def get_python(message):
    start_code_block = message.find("```Python")
    if start_code_block == -1:
        start_code_block = message.find("```python")
    if start_code_block == -1:
        start_code_block = message.find("```")
        cut_string = message[start_code_block + 3:]
    else:
        cut_string = message[start_code_block + 10:]
    end_code_block = cut_string.find("```")
    return cut_string[:end_code_block].strip()

# Helper function to format the model name for file naming
def format_model_name(model_name):
    if ":" in model_name:
        parts = model_name.split(":", 1)
        return f"{parts[0]}-{parts[1]}"
    else:
        return model_name
