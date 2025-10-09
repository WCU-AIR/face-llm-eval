import os
import ollama
import time
import json

from utilities import api_call, get_python, format_model_name

# Ensure execution always happens from face-llm-eval/src
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..")) 
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
os.chdir(SRC_DIR)

# Adjust this as needed!
model = "qwen2.5-coder:7b"


client = ollama.Client(host="localhost:11434")
with open("../json/kattis_problems.json", "r") as file:
    kattis_problems = json.load(file)

total = len(kattis_problems)

print(f"Preloading {model} ...")
start_time = time.perf_counter()
client.chat(model=model, messages=[{"role": "user", "content": ""}])
end_time = time.perf_counter()
load_time = end_time - start_time
print(f"Loading completed in {load_time} seconds")
        
solutions_file = f"../json/kattis_solutions_{format_model_name(model)}_test.json"

### Setup counters
counter = 0
total_time = 0
problems = {}
for problem in kattis_problems:
    counter += 1
    # Print every 500 problems
    if counter % 500 == 0:
        print(f"After {counter} problems, total generation time is {total_time}")

    problems[problem] = {}
    problems[problem]["id"] = problem
    problems[problem]["model"] = model
    problems[problem]["api_times"] = []
    problems[problem]["api_responses"] = []
    problems[problem]["python_clean"] = []
    # Combine problem description and test cases
    input_text = kattis_problems[problem]["description"] + "\n The availalble tests with input and output formats are: \n" + kattis_problems[problem]["tests"] 

    # Make API call to generate Python solution
    start_time = time.perf_counter()
    api_answer = api_call(input_text, model, client)
    end_time = time.perf_counter()
    api_time = end_time - start_time
    total_time += api_time
    problems[problem]["api_times"].append(api_time)
    problems[problem]["api_responses"].append(api_answer)
    
    print(f"{problem}: Solution generation time is {api_time} with difficulty {kattis_problems[problem]['difficulty_elo']}")
        
    # Get the Python code from Ollama output
    api_python = get_python(api_answer)
    problems[problem]["python_clean"].append(api_python)


    with open(solutions_file, 'w') as file:
        json.dump(problems, file, indent=2)
