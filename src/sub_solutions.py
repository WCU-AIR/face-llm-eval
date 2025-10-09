import os
import subprocess
import time
import json
import random
import argparse
import sys
from utilities import get_last_non_empty_line, get_test_cases_info

# Ensure execution always happens from face-llm-eval/src
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..")) 
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
os.chdir(SRC_DIR)

# Argument parsing for cli
parser = argparse.ArgumentParser(description="Process Kattis submissions.")
parser.add_argument(
    "-m", "--model", 
    type=str, 
    required=True, 
    help="Specify the model name (ex. qwen2.5-coder-7b, codeqwen-7b, deepseek-coder-6.7b, etc)"
)
args = parser.parse_args()
MODEL = args.model

# Directories and file paths
solution_dir = "../json"
output_dir = solution_dir
os.makedirs(output_dir, exist_ok=True)

# Define files
input_file = os.path.join(solution_dir, f"kattis_solutions_{MODEL}.json")
output_file = os.path.join(output_dir, f"submissions_{MODEL}.json")
temp_file = output_file + ".tmp"
checkpoint_file = os.path.join(output_dir, "checkpoint.txt")

# Load existing results if exists
if os.path.exists(output_file):
    with open(output_file, "r") as f:
        new_results = json.load(f)
else:
    new_results = {}

# Read the last checkpointed problem ID
def read_checkpoint():
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, "r") as f:
            return f.read().strip()
    return None

# Write the latest problem ID to checkpoint
def write_checkpoint(problem_id):
    with open(checkpoint_file, "w") as f:
        f.write(problem_id)

# Load last checkpointed ID
last_saved_id = read_checkpoint()

# Load solutions
with open(input_file, "r") as file:
    kattis_problems = json.load(file)

print(f"Problem counts: {len(kattis_problems)}")

# Initializing a problem count to amount of pre processed problems
problem_count = len(new_results)
skipped_count = 0

for problem_id in kattis_problems:
    # Print every 100 problems
    if problem_count % 100 == 0:
        print(f"Processing problem {problem_count}")

    # Skip if already processed and checkpointed
    if problem_id in new_results:
        skipped_count += 1
        continue
    
    problem_count += 1

    if skipped_count > 0:
        print(f"Skipped {skipped_count} problems!")
        skipped_count = 0
    
    # Get solution
    try:
        api_python = kattis_problems[problem_id]["python_clean"][0]
    except (KeyError, IndexError):
        print(f"Skipping {problem_id} - no code found")
        continue

    with open("tmp.py", "w") as f:
        f.write(api_python)

    # Ensure .kattisrc exists
    kattisrc_path = os.path.join(SRC_DIR, ".kattisrc")
    if not os.path.exists(kattisrc_path):
        print("Error: .kattisrc file not found in src directory.")
        print("Please copy or configure your .kattisrc before running submissions.")
        sys.exit(1)

    # Submit solution
    submit_script = os.path.join(os.getcwd(), "submit.py")
    result = subprocess.run(
        ["python3", submit_script, "-p", problem_id, "tmp.py", "-f"],
        capture_output=True,
        text=True
    )

    status_line = get_last_non_empty_line(result.stdout)
    status = status_line.split(":")[-1].strip() if status_line else "Unknown"
    passed, total = get_test_cases_info(result.stdout)

    if "token" in result.stdout.lower() or "token" in result.stderr.lower():
        print(f"Error, Rate limited at problem {problem_id}")

    # Store results
    new_results[problem_id] = {
        "id": problem_id,
        "status": status,
        "cases_passed": [passed, total]
    }

    # Save to file after each submission with atomic write
    with open(temp_file, "w") as f:
        json.dump(new_results, f, indent=2, sort_keys=True)
        f.flush()
        os.fsync(f.fileno())
    os.replace(temp_file, output_file)
    write_checkpoint(problem_id)  # Update checkpoint

    # print(result.stdout) Optional to see output from Kattis
    
    # Random sleep between 60 to 100 seconds to avoid rate limiting
    time.sleep(random.uniform(60, 100))

print("Complete!")
