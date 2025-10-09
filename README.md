# face-llm-eval

A lightweight evaluation framework used to generate and submit Python solutions to Kattis problems using locally-hosted LLM models (via Ollama). This repository was developed as part of a research project and is suitable for demos and reproducible experiments. 


## Prerequisites

1. Python 3.x 

2. Ollama installed and running locally if you plan to generate model outputs. Follow the official instructions at https://ollama.com/download. Pull a model you want to use (example name used in repository: `qwen2.5-coder:7b`).

3. A Kattis account and your `.kattisrc` file placed inside the `src/` directory. See https://open.kattis.com/info/submit for how to retrieve your personal `.kattisrc`.


## Quickstart (generate + submit)

1. Prepare environment and install `ollama` Python client (see Prerequisites).

2. Start Ollama and make sure your model is downloaded locally, or adjust the `model` variable in `src/gen_solutions.py`.

3. Generate solutions (this writes to a file in `json/`). Edit the `model` variable in `src/gen_solutions.py` then run:

	```bash
	python3 src/gen_solutions.py
	```

	Output: `json/kattis_solutions_<model>_test.json`.

4. Submit solutions to Kattis (make sure `.kattisrc` is in `src/`). The submission script expects a model identifier; pass the same model name used while generating solutions:

	```bash
	python3 src/sub_solutions.py -m qwen2.5-coder-7b
	```

	Output: `json/submissions_qwen2.5-coder-7b.json` and `json/checkpoint.txt` that stores the last submitted problem id.

Note: `sub_solutions.py` sleeps randomly between submissions (60–100s) to avoid rate limits. 

## Large Scale Evaluation
If you wish to replicate or extend this experiment at a larger scale, as done in our paper, refer to the original FACE repository (https://github.com/linhbngo/llama-kattis).
You’ll need to convert the problems found in the automining directory into a single JSON file containing all problems, formatted in the same style as `kattis_problems.json`.

## Paper showcase
Add paper info here

---