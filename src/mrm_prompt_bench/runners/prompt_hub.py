import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from collections import defaultdict
from typing import List, Dict, Optional

# === Helper: Extract Response After </think> ===

def extract_post_think(text: str) -> str:
    """
    Extracts the content after the </think> tag.
    If the tag is not found, returns the full string.
    """
    return text.split("</think>")[-1].strip() if "</think>" in text else text.strip()

# === 1. Load Model and Tokenizer ===

def load_model(model_name="deepseek-ai/deepseek-llm-7b-chat"):
    """
    Loads tokenizer and model from HuggingFace with correct dtype and device mapping.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype=torch.float16)
    model.eval()
    return tokenizer, model

# === 2. Generate Prompt Variants ===

def generate_prompt_variants(
    guideline: str,
    context: str,
    strategy: str,
    tokenizer,
    model,
    num_variants=3,
    few_shot_examples: Optional[List[str]] = None,
    temperature=0.7
) -> List[str]:
    """
    Generates multiple prompt variants using a specified prompting strategy.
    Supports chain-of-thought, tree-of-thought, few-shot, and zero-shot.
    """
    strategy_instruction_map = {
        "cot": "Use a step-by-step reasoning approach (Chain-of-Thought).",
        "tot": "Use a tree-structured reasoning pattern (Tree-of-Thought).",
        "few_shot": "Follow the format of the few-shot examples provided.",
        "zero_shot": "Answer the task without any example, using general knowledge."
    }

    example_block = ""
    if strategy == "few_shot" and few_shot_examples:
        example_block = "\n\n".join(f"Example {i+1}:\n{ex}" for i, ex in enumerate(few_shot_examples))

    prompt_template = f"""
Instruction: {guideline}
Context: {context}
{strategy_instruction_map.get(strategy, '')}

{example_block}

Now, generate a prompt that instructs an LLM to perform this task.
"""
    input_ids = tokenizer(prompt_template, return_tensors="pt").input_ids.to(model.device)

    outputs = model.generate(
        input_ids=input_ids,
        max_new_tokens=80,
        num_return_sequences=num_variants,
        do_sample=True,
        temperature=temperature
    )

    return [extract_post_think(tokenizer.decode(output, skip_special_tokens=True)) for output in outputs]

# === 3. Score Prompts Using Log-Likelihood ===

def compute_log_likelihood(prompt: str, tokenizer, model) -> float:
    """
    Computes a proxy for log-likelihood by calculating negative loss times token count.
    Used to rank prompt candidates by model confidence.
    """
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model(**inputs, labels=inputs["input_ids"])
        loss = outputs.loss.item()
    return -loss * inputs["input_ids"].shape[1]

# === 4. Build Prompt Hub ===

def build_prompt_hub(
    validation_data: Dict[str, Dict[str, List[Dict]]],
    tokenizer,
    model,
    strategy="cot"
) -> Dict:
    """
    Iterates over validation data and generates scored prompt variants for each guideline.
    Returns a nested dictionary of template → section → prompt set.
    """
    prompt_hub = defaultdict(lambda: defaultdict(list))

    for template, sections in validation_data.items():
        for section, guideline_blocks in sections.items():
            for block in guideline_blocks:
                guideline = block["guideline"]
                context = block.get("context", "")
                examples = block.get("few_shot_examples", [])

                prompt_variants = generate_prompt_variants(
                    guideline=guideline,
                    context=context,
                    strategy=strategy,
                    tokenizer=tokenizer,
                    model=model,
                    few_shot_examples=examples
                )
                scored_prompts = [
                    {
                        "text": p,
                        "log_likelihood": compute_log_likelihood(p, tokenizer, model)
                    }
                    for p in prompt_variants
                ]
                scored_prompts.sort(key=lambda x: x["log_likelihood"], reverse=True)

                prompt_hub[template][section].append({
                    "guideline": guideline,
                    "strategy": strategy,
                    "prompts": scored_prompts
                })
    return prompt_hub

# === 5. Example Usage ===

if __name__ == "__main__":
    validation_templates = {
        "Credit Risk Template": {
            "Model Framework": [
                {
                    "guideline": "Assess whether the model objectives align with the core model requirements.",
                    "context": "The model aims to detect risk in small business loans. Core requirements include fairness, explainability, and compliance.",
                    "few_shot_examples": [
                        "Prompt: Evaluate whether the objectives defined in the document are supported by technical and compliance requirements.",
                        "Prompt: Analyze how the model design principles align with the original goals stated for the risk prediction.",
                        "Prompt: Determine whether core compliance constraints are reflected in the model objectives."
                    ]
                }
            ]
        }
    }

    tokenizer, model = load_model()
    hub = build_prompt_hub(validation_templates, tokenizer, model, strategy="few_shot")

    print(json.dumps(hub, indent=2))



-------

The line of code that computes the log-likelihood is:

return -loss * inputs["input_ids"].shape[1]  # Approximate log-likelihood

This line appears inside the compute_log_likelihood() function and it does the following:
	•	loss: is the average negative log-likelihood per token, computed internally by the model.
	•	inputs["input_ids"].shape[1]: gives the number of tokens in the input.
	•	-loss * number_of_tokens: gives the total (unnormalized) log-likelihood for the full prompt.

This multiplication converts the per-token loss into an estimate of the full sequence log-likelihood. The negative sign flips it from a loss (lower is better) to a log-likelihood (higher is better).

The line that calculates the loss is:

outputs = model(**inputs, labels=inputs["input_ids"])
loss = outputs.loss.item()

Here’s what’s happening:
	•	model(**inputs, labels=inputs["input_ids"]): This feeds the input tokens into the model and tells it to compute the loss by comparing the model’s predictions to the same input tokens (this is how language models are typically trained and evaluated).
	•	outputs.loss: This is the cross-entropy loss returned by the model.
	•	.item(): Extracts the scalar float value from the tensor.

So, this line effectively computes the average negative log-likelihood per token.


--------

Great question!

The example_block = "" line in your code acts as a default when no few_shot_examples are supplied. If you’re using a strategy like "few_shot", you should supply a list of curated example prompts. Here’s how you can populate it for testing:

⸻

Example Use Case: Model Validation Instruction

Instruction: “Assess whether the model objectives align with the core model requirements.”

Example Few-Shot Prompts (3):

few_shot_examples = [
    "Prompt: Evaluate whether the model's objectives address the business and regulatory constraints stated in the MDD.",
    "Prompt: Review if the defined model goals comply with documented core requirements such as fairness and explainability.",
    "Prompt: Check the alignment between technical objectives and risk management principles described in the development framework."
]

You can plug this list directly into the example_block creation inside generate_prompt_variants() like so:

if strategy == "few_shot" and few_shot_examples:
    example_block = "\n\n".join(f"Example {i+1}:\n{ex}" for i, ex in enumerate(few_shot_examples))

Full Test Snippet

You can try this sample directly to test the pipeline:

test_guideline = "Assess whether the model objectives align with the core model requirements."
test_context = "The model aims to predict loan risk. Core requirements include interpretability, regulatory alignment, and model robustness."
test_examples = [
    "Prompt: Evaluate whether the model's objectives address the business and regulatory constraints stated in the MDD.",
    "Prompt: Review if the defined model goals comply with documented core requirements such as fairness and explainability.",
    "Prompt: Check the alignment between technical objectives and risk management principles described in the development framework."
]

Then call:

generate_prompt_variants(
    guideline=test_guideline,
    context=test_context,
    strategy="few_shot",
    tokenizer=your_tokenizer,
    model=your_model,
    few_shot_examples=test_examples
)
