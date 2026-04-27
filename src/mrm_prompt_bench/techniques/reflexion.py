import openai
import os

# Set your API key securely
openai.api_key = "your_openai_api_key"  # or use os.environ["OPENAI_API_KEY"]

system_prompt = "You are an expert model validation reviewer. You generate and evaluate validation report text based on regulatory and MRM expectations."

def call_llm(prompt, temperature=0.3):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature
    )
    return response.choices[0].message["content"].strip()

# Step 1: Initial generation
def generate_initial_response(instruction, context):
    prompt = f"Validation Instruction:\n{instruction}\n\nContext:\n{context}\n\nWrite a validation paragraph based on the instruction and the context."
    return call_llm(prompt)

# Step 2: Reflection
def generate_reflection(instruction, context, response):
    prompt = f"""
You are reviewing your own generated validation report text. Provide a structured critique.

Instruction:
{instruction}

Context:
{context}

Your Response:
{response}

Evaluate the response on:
1. Relevancy to the instruction
2. Completeness — whether all required content is present
3. Specificity — whether claims are grounded in the context

Then suggest improvements.

Return your output in this format:
{{
"Relevancy": int (1-5),
"Completeness": int (1-5),
"Specificity": int (1-5),
"Critique": "...",
"Suggestion": "..."
}}
"""
    return call_llm(prompt)

# Step 3: Regeneration
def regenerate_with_reflection(instruction, context, reflection):
    prompt = f"""Instruction: {instruction}
Context: {context}

Here is feedback on your previous response:
{reflection}

Write an improved validation response based on this feedback."""
    return call_llm(prompt)

# Example run
instruction = "Assess whether the model objectives align with the core model requirements."
context = """
Section 2.1 - Model Objectives:
The model aims to identify potential instances of financial abuse in banking transactions involving elderly customers.

Section 2.2 - Core Model Requirements:
- Detect subtle patterns indicative of abuse
- Operate within bank data privacy constraints
- Provide interpretable outputs for compliance
- Achieve at least 85% precision and 80% recall
"""

initial = generate_initial_response(instruction, context)
reflection = generate_reflection(instruction, context, initial)
improved = regenerate_with_reflection(instruction, context, reflection)

print("Initial Response:\n", initial)
print("\nReflection:\n", reflection)
print("\nImproved Response:\n", improved)