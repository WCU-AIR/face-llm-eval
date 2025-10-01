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
