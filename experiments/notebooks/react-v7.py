import json
import os
import time

import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

RELEVANCY_THRESHOLD = 4.0
MAX_ITERATIONS = 5

system_prompt = "You are an AI assisting with model validation."


def call_llm(prompt, temperature=0.3, max_tokens=500, system_prompt=""):
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return response["choices"][0]["message"]["content"]


def evaluate_context_quality(context, validation_instruction, max_retries=2):
    """
    Evaluate retrieved context against a validation instruction using:
    - Relevancy
    - Completeness
    - Specificity

    Each criterion includes both a numeric score (1-5) and justification.
    """
    evaluation_prompt = f"""
Evaluate the following retrieved context in relation to the validation instruction using three criteria:

1. Relevancy – How directly does the context address the instruction?
2. Completeness – Are all required elements present to answer the instruction fully?
3. Specificity – Does the context cite specific items (terms, metrics, definitions) from the document?

Validation Instruction:
"{validation_instruction}"

Retrieved Context:
"{context}"

Return your evaluation as a JSON object in the following format:

{{
  "Relevancy": {{
    "Score": X,
    "Justification": "Explanation for why this score was given for relevancy..."
  }},
  "Completeness": {{
    "Score": Y,
    "Justification": "Explanation for completeness..."
  }},
  "Specificity": {{
    "Score": Z,
    "Justification": "Explanation for specificity..."
  }}
}}

Where X, Y, Z are scores from 1 (very poor) to 5 (excellent).
Do not include any commentary outside the JSON structure.
"""

    for attempt in range(max_retries):
        response = call_llm(evaluation_prompt, temperature=0.3)

        try:
            scores = json.loads(response.strip())
            if all(metric in scores for metric in ["Relevancy", "Completeness", "Specificity"]):
                avg_score = (
                    scores["Relevancy"]["Score"]
                    + scores["Completeness"]["Score"]
                    + scores["Specificity"]["Score"]
                ) / 3
                return avg_score, scores
        except Exception:
            pass  # Optionally log the response here for debugging

    # Fallback if parsing fails
    return 0.0, {
        "Relevancy": {"Score": 0, "Justification": "Parsing failed."},
        "Completeness": {"Score": 0, "Justification": "Parsing failed."},
        "Specificity": {"Score": 0, "Justification": "Parsing failed."}
    }

def react_validation_assessment(validation_instruction, text):
    """
    Implements the ReAct framework for validation assessment.
    Iterates dynamically until relevancy threshold is reached.
    """
    reasoning_steps = []
    context = ""  # Start with an empty context
    iteration = 0
    relevancy_score = 0  # Initialize relevancy score

    while relevancy_score < RELEVANCY_THRESHOLD and iteration < MAX_ITERATIONS:
        iteration += 1
        print("\n" + "-" * 60)
        print(f"Iteration {iteration}...")

        # 1. Thought Generation
        thought_prompt = f"""
        Given the validation instruction: "{validation_instruction}"
        and the retrieved context: "{context}"
        What additional information is needed for a thorough assessment?
        """
        thought = call_llm(thought_prompt, temperature=0.3, max_tokens=500, system_prompt=system_prompt)
        print("\nThought Prompt:\n", thought_prompt)
        print("Generated Thought:\n", thought)
        reasoning_steps.append(f"Thought {iteration}: {thought}")

        # 2. Action Selection (Query Formulation)
        action_prompt_for_query_formulation = f"""
        Based on the thought: "{thought}"
        Formulate a query to retrieve missing contextual details from the Model Development Document.
        """
        action_1 = call_llm(action_prompt_for_query_formulation, temperature=0.3, max_tokens=500, system_prompt=system_prompt)
        print("\nQuery Formulation Prompt:\n", action_prompt_for_query_formulation)
        print("Generated Action (Query):\n", action_1)
        reasoning_steps.append(f"Action {iteration} (Query Formulation): {action_1}")

        # 3. Retrieve context (simulated)
        action_prompt_retrieve_context = f"""
        Answer the QUERY using the provided CONTEXT.
        QUERY: "{action_1}"
        CONTEXT: "{text}"
        """
        additional_context = call_llm(action_prompt_retrieve_context, temperature=0.3, max_tokens=500, system_prompt="")
        print("\nRetrieve Context Prompt:\n", action_prompt_retrieve_context)
        print("Retrieved Additional Context:\n", additional_context)
        reasoning_steps.append(f"Action {iteration} (Context Retrieved): {additional_context}")

        # 4. Evaluate Retrieved Context Quality (enhanced with reasoning)
        avg_score, scores = evaluate_context_quality(additional_context, validation_instruction)
        relevancy_score = avg_score

        print("\nContext Evaluation Scores:")
        for metric, data in scores.items():
            print(f"{metric}: {data['Score']} — {data.get('Justification', '')}")
        print(f"Average Relevancy Score: {avg_score}")

        if relevancy_score >= RELEVANCY_THRESHOLD:
            print("\nSufficient relevant context retrieved. Proceeding to report generation...")
            context += "\n" + additional_context  # Append final high-relevancy context
            break
        else:
            print("\nContext not relevant enough, refining search...")
            time.sleep(2)

    # 5. Final Report Generation
    report_prompt = f"""
    Based on the final observations and retrieved context, generate a structured validation report.
    Validation Assessment: {validation_instruction}
    Context: {context}
    Provide a detailed and structured response.
    """
    validation_report = call_llm(report_prompt, temperature=0.7, max_tokens=2000, system_prompt=system_prompt)
    print("\nFinal Report Prompt:\n", report_prompt)
    print("Generated Validation Report:\n", validation_report)
    
    return validation_report, reasoning_steps