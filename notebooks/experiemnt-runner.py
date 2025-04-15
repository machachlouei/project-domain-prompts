# Integrated Experimental Runner for EFA LLM Prompting Study

import json
import random
from datetime import datetime

# Configurations
CONFIG = {
    "temperature": 0.3,
    "top_p": 0.95,
    "max_tokens": 600,
    "models": ["gpt-4o", "llama3", "qwen7b"],
    "prompting_techniques": ["zero_shot"],
    "repetitions": 3
}

# Sample prompt template
PROMPT_TEMPLATE = """
Instruction: {instruction}

Context:
{context}

Please generate a response based on the instruction and context above.
"""

# Load input data
def load_data(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

# Generate prompt
def generate_prompt(instruction, context, technique):
    # Extendable: use different templates per technique
    return PROMPT_TEMPLATE.format(instruction=instruction, context=context)

# Simulated model response (placeholder for actual API or local model)
def query_model(prompt, model_name):
    return f"[Simulated response from {model_name} using prompt: {prompt[:60]}...]"

# Evaluation logic
def evaluate_response(instruction, context, response):
    return {
        "relevancy": {
            "score": random.randint(3, 5),
            "rationale": "Covers instruction topic adequately."
        },
        "completeness": {
            "score": random.randint(3, 5),
            "rationale": "Includes most key elements."
        },
        "specificity": {
            "score": random.randint(2, 5),
            "rationale": "Mentions document-specific terms."
        },
        "errors": {
            "hallucination": {
                "exists": random.choice([True, False]),
                "evidence": "Mentions a feature not present in context." if random.choice([True, False]) else "",
                "severity": random.choice(["low", "medium", "high"])
            },
            "redundancy": {
                "exists": random.choice([True, False]),
                "evidence": "Repeats same phrase or point.",
                "severity": random.choice(["low", "medium"])
            },
            "lack_of_specificity": {
                "exists": random.choice([True, False]),
                "evidence": "Uses vague terms without citing context.",
                "severity": random.choice(["low", "medium", "high"])
            }
        }
    }

# Save output
def save_output(output, filepath):
    with open(filepath, "w") as f:
        json.dump(output, f, indent=2)

# Run experiment
def run_experiment(input_path, output_dir):
    data = load_data(input_path)
    for entry in data:
        for technique in CONFIG["prompting_techniques"]:
            for model in CONFIG["models"]:
                for rep in range(CONFIG["repetitions"]):
                    prompt = generate_prompt(entry["instruction"], entry["context"], technique)
                    response = query_model(prompt, model)
                    evaluation = evaluate_response(entry["instruction"], entry["context"], response)
                    
                    result = {
                        "id": entry["id"],
                        "instruction": entry["instruction"],
                        "context": entry["context"],
                        "model": model,
                        "prompting_technique": technique,
                        "prompt": prompt,
                        "response": response,
                        "evaluation": evaluation,
                        "generation_metadata": {
                            "temperature": CONFIG["temperature"],
                            "top_p": CONFIG["top_p"],
                            "max_tokens": CONFIG["max_tokens"],
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                    
                    output_filename = f"{entry['id']}_{model}_{technique}_rep{rep+1}.json"
                    save_output(result, f"{output_dir}/{output_filename}")

# Example run (simulate)
if __name__ == "__main__":
    sample_input = [
        {
            "id": "001",
            "instruction": "Assess whether core model requirements align with model objectives.",
            "context": "The model is designed to detect risk segments using logistic regression trained on internal behavioral data..."
        }
    ]
    with open("/mnt/data/sample_input.json", "w") as f:
        json.dump(sample_input, f)

    run_experiment("/mnt/data/sample_input.json", "/mnt/data")
