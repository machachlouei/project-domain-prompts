import openai
import json

# OpenAI API Key
OPENAI_API_KEY = "your_openai_api_key"
openai.api_key = OPENAI_API_KEY

# Evaluation Metrics Thresholds
EVALUATION_THRESHOLDS = {
    "Relevancy": 4.0,  # Minimum acceptable score
    "Hallucination": 2.0,  # Lower is better
    "Groundedness": 4.0,
    "Comprehensiveness": 4.0
}

# Sample validation assessment instruction
validation_instruction = """
Assess whether the model's assumptions and theoretical framework are consistent with best practices.
Examine if the validation report provides a clear assessment of model risks and mitigation strategies.
"""

# ReAct-CoT Prompt Function
def react_cot_prompt(input_text):
    return f"""
    You are an expert model validator using the ReAct framework. 
    Your task is to generate a validation report while dynamically retrieving additional context if needed.
    
    Step 1: Identify key validation objectives.
    Step 2: Retrieve any relevant theoretical background if needed.
    Step 3: Apply structured analysis to check model assumptions and framework.
    Step 4: Evaluate risks and mitigation strategies.
    Step 5: Assess output quality based on Relevancy, Hallucination, Groundedness, and Comprehensiveness.
    Step 6: If evaluation scores are below threshold, refine the report.

    Instruction:
    {input_text}

    Generate a well-structured validation report.
    """

# Function to generate validation report using GPT-4 API
def generate_validation_report(instruction):
    prompt = react_cot_prompt(instruction)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an expert model validator."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# Function to evaluate generated report
def evaluate_generated_report(report):
    evaluation_prompt = f"""
    Evaluate the following AI-generated validation report based on:
    
    1. Relevancy (1-5): Does it address key aspects of the problem?
    2. Hallucination (1-5): Does it introduce false information?
    3. Groundedness (1-5): Are claims well-supported?
    4. Comprehensiveness (1-5): Does it provide a full assessment?

    Generated Report:
    {report}

    Provide JSON output with scores for each metric.
    """
    evaluation_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a senior model validation evaluator."},
                  {"role": "user", "content": evaluation_prompt}]
    )
    return json.loads(evaluation_response["choices"][0]["message"]["content"])

# Function to check if output meets quality thresholds
def meets_quality_thresholds(scores, thresholds):
    return all(scores[metric] >= thresholds[metric] for metric in thresholds)

# Iterative ReAct Evaluation Loop
def iterative_evaluation(instruction, max_iterations=3):
    iteration = 0
    while iteration < max_iterations:
        print(f"\n🔄 Iteration {iteration + 1}: Generating Validation Report...")
        generated_report = generate_validation_report(instruction)
        
        print("\n🔍 Evaluating Generated Report...")
        llm_scores = evaluate_generated_report(generated_report)

        print("\n📊 LLM Evaluation Scores:")
        print(llm_scores)

        if meets_quality_thresholds(llm_scores, EVALUATION_THRESHOLDS):
            print("\n✅ Report meets quality criteria. Finalizing output.")
            return generated_report, llm_scores
        else:
            print("\n⚠️ Report does NOT meet quality criteria. Refining response...\n")
            iteration += 1

    print("\n❌ Maximum iterations reached. Returning best attempt.")
    return generated_report, llm_scores

# Run Experiment
if __name__ == "__main__":
    final_report, final_scores = iterative_evaluation(validation_instruction)

    print("\n🔹 Final Generated Validation Report:")
    print(final_report)

    print("\n🔹 Final Evaluation Scores:")
    print(final_scores)