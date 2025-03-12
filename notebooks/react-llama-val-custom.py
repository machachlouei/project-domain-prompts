import time
import requests

# Define API Endpoint and API Key for Local Llama Server
API_ENDPOINT = "http://localhost:5000/v1/completions"  # Modify if using a different endpoint

# Predefined validation assessment instruction
validation_instruction = "Assess whether core requirements align with model objectives."

# Simulated retrieved context (In real implementation, use a RAG pipeline)
contextual_information = """
Model Development Document (MDD) Excerpt:
- Model Objective: Ensure generalization across different customer segments.
- Core Requirements: Must perform well on historical data, but does not explicitly mention segmentation validation.
"""

# Function to call Llama-3.2-3b-Instruct
def call_llm(prompt, temperature=0.3, max_tokens=500):
    payload = {
        "model": "llama-3.2-3b-instruct",
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    response = requests.post(API_ENDPOINT, json=payload)
    return response.json()["choices"][0]["text"].strip()

# Lower temperature (0.3 - 0.5) for reasoning and evaluation to ensure deterministic and accurate assessments.
# Slightly higher temperature (0.7) for generation to allow some variability in generating validation reports.

# ReAct Algorithm Implementation
def react_validation_assessment(validation_instruction, context, max_iterations=3):
    """
    Implements the ReAct framework for validation assessment.
    Uses an iterative approach to refine reasoning, retrieve additional context, and generate a report.
    """
    reasoning_steps = []
    for iteration in range(max_iterations):
        print(f"Iteration {iteration + 1}...")

        # 1. Thought Generation (Low Temperature for Accuracy)
        thought_prompt = f"""
        Given the validation instruction: "{validation_instruction}"
        and the retrieved context: "{context}"
        What additional information is needed for a thorough assessment?
        """
        thought = call_llm(thought_prompt, temperature=0.3)
        reasoning_steps.append(f"Thought {iteration+1}: {thought}")

        # 2. Action Selection (Retrieve More Context)
        action_prompt = f"""
        Based on the thought: "{thought}"
        Formulate a query to retrieve missing contextual details from the Model Development Document.
        """
        action = call_llm(action_prompt, temperature=0.3)
        reasoning_steps.append(f"Action {iteration+1}: {action}")

        # Simulating context retrieval (In real use, connect to a RAG system)
        additional_context = f"Retrieved context: Simulated additional information based on: {action}"
        context += "\n" + additional_context

        # 3. Observation Collection
        observation_prompt = f"""
        Using the updated context: "{context}"
        Provide an observation regarding how core requirements align with model objectives.
        """
        observation = call_llm(observation_prompt, temperature=0.3)
        reasoning_steps.append(f"Observation {iteration+1}: {observation}")

        # Check if enough context has been retrieved
        if "sufficient" in observation.lower():
            print("Enough context retrieved. Proceeding to report generation...")
            break

        time.sleep(2)  # Avoid hitting API rate limits

    # 4. Final Validation Report Generation (Higher Temperature for More Variability)
    report_prompt = f"""
    Based on the final observations and retrieved context, generate a structured validation report.
    Validation Assessment: {validation_instruction}
    Context: {context}
    Provide a detailed and structured response.
    """
    validation_report = call_llm(report_prompt, temperature=0.7)  # Slightly higher for diverse generation
    return validation_report, reasoning_steps

# Run ReAct-based Validation Assessment
generated_report, reasoning_trace = react_validation_assessment(validation_instruction, contextual_information)

# Print the validation report
print("\nGenerated Validation Report:\n")
print(generated_report)

# Print the reasoning steps (debugging)
print("\nReAct Reasoning Trace:\n")
for step in reasoning_trace:
    print(step)

# Automated Evaluation of the Generated Report
def evaluate_report(report, context):
    """
    Uses another LLM to assess the generated report based on evaluation metrics:
    - Relevancy
    - Hallucination
    - Comprehensiveness
    - Groundedness
    """
    evaluation_prompt = f"""
    Evaluate the following validation report based on the retrieved context.
    Validation Report: "{report}"
    Context: "{context}"
    
    Provide scores from 1 to 5 for the following criteria:
    1. Relevancy (Does the report answer the validation instruction?)
    2. Hallucination (Does the report introduce incorrect or unsupported information?)
    3. Comprehensiveness (Does the report cover all key aspects?)
    4. Groundedness (Is the report supported by the retrieved context?)
    
    Format your response as:
    Relevancy: X
    Hallucination: X
    Comprehensiveness: X
    Groundedness: X
    """
    evaluation_result = call_llm(evaluation_prompt, temperature=0.3)  # Low temperature for consistency
    return evaluation_result

# Run Evaluation
evaluation_scores = evaluate_report(generated_report, contextual_information)

# Print Evaluation Scores
print("\nEvaluation Scores:\n")
print(evaluation_scores)