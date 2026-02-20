import openai
import time
import json
import re

# Set your OpenAI API key
openai.api_key = "your_openai_api_key"

RELEVANCY_THRESHOLD = 4.0
MAX_ITERATIONS = 5

def call_llm(prompt, temperature=0.3, max_tokens=500, system_prompt="You are an expert model validation reviewer."):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response["choices"][0]["message"]["content"]

def evaluate_context_quality(context, validation_instruction, max_retries=2):
    evaluation_prompt = f"""
Evaluate the following retrieved context in relation to the validation instruction using three criteria:

1. Relevancy – How directly does the context address the instruction?
2. Completeness – Are all required elements present to answer the instruction fully?
3. Specificity – Does the context cite specific items (terms, metrics, definitions) from the document?

Validation Instruction:
"{validation_instruction}"

Retrieved Context:
"{context}"

Return your scores and justifications as a valid JSON object using this format:
{{
  "Relevancy": {{"score": X, "justification": "..." }},
  "Completeness": {{"score": X, "justification": "..." }},
  "Specificity": {{"score": X, "justification": "..." }}
}}

Where X is a number from 1 (very poor) to 5 (excellent).
"""

    for attempt in range(max_retries):
        response = call_llm(evaluation_prompt, temperature=0.3)

        try:
            result = json.loads(response.strip())
            scores = {k: v["score"] for k, v in result.items()}
            avg_score = sum(scores.values()) / 3
            return avg_score, result
        except Exception:
            try:
                scores = {
                    "Relevancy": int(re.search(r'Relevancy.*?(\d)', response, re.IGNORECASE).group(1)),
                    "Completeness": int(re.search(r'Completeness.*?(\d)', response, re.IGNORECASE).group(1)),
                    "Specificity": int(re.search(r'Specificity.*?(\d)', response, re.IGNORECASE).group(1))
                }
                avg_score = sum(scores.values()) / 3
                return avg_score, scores
            except:
                continue
    return 0.0, {"Relevancy": 0, "Completeness": 0, "Specificity": 0}

#another version of evaluate-context-quality
def evaluate_context_quality(context, validation_instruction, max_retries=2):
    evaluation_prompt = f"""
Evaluate the following retrieved context in relation to the validation instruction using three criteria:

1. Relevancy – How directly does the context address the instruction?
2. Completeness – Are all required elements present to answer the instruction fully?
3. Specificity – Does the context cite specific items (terms, metrics, definitions) from the document?

Validation Instruction:
"{validation_instruction}"

Retrieved Context:
"{context}"

Return your scores and justifications as a valid JSON object using this format:
{{
  "Relevancy": {{"score": X, "justification": "..." }},
  "Completeness": {{"score": X, "justification": "..." }},
  "Specificity": {{"score": X, "justification": "..." }}
}}

Where X is a number from 1 (very poor) to 5 (excellent).
"""

    for attempt in range(max_retries):
        response = call_llm(evaluation_prompt, temperature=0.3)

        # Try parsing as proper JSON with justification
        try:
            result = json.loads(response.strip())
            scores = {k: v["score"] for k, v in result.items()}
            avg_score = sum(scores.values()) / 3
            return avg_score, result
        except Exception:
            pass

        # Fallback regex-based score and justification extraction
        try:
            def extract_metric(name):
                score_match = re.search(fr'{name}\s*[:=]\s*(\d)', response, re.IGNORECASE)
                justification_match = re.search(fr'{name}.*?(?:score\s*[:=]\s*\d[^\n]*[\n]*)?(.*?)(?=\n\S|\Z)', response, re.IGNORECASE | re.DOTALL)
                score = int(score_match.group(1)) if score_match else 0
                justification = justification_match.group(1).strip() if justification_match else "No justification found."
                return {"score": score, "justification": justification}

            fallback_result = {
                "Relevancy": extract_metric("Relevancy"),
                "Completeness": extract_metric("Completeness"),
                "Specificity": extract_metric("Specificity")
            }
            avg_score = sum([v["score"] for v in fallback_result.values()]) / 3
            return avg_score, fallback_result
        except:
            continue

    # If all attempts fail
    return 0.0, {
        "Relevancy": {"score": 0, "justification": "N/A"},
        "Completeness": {"score": 0, "justification": "N/A"},
        "Specificity": {"score": 0, "justification": "N/A"}
    }
    
def run_react(validation_instruction, document_text):
    reasoning_steps = []
    context = ""
    iteration = 0
    relevancy_score = 0

    while relevancy_score < RELEVANCY_THRESHOLD and iteration < MAX_ITERATIONS:
        iteration += 1
        print(f"\n--- ReAct Iteration {iteration} ---")

        thought_prompt = f"""
Given the validation instruction: "{validation_instruction}"
and the retrieved context: "{context}"
What additional information is needed for a thorough assessment?
"""
        thought = call_llm(thought_prompt)
        print(f"Thought Prompt: {thought_prompt}\nThought Response: {thought}")
        reasoning_steps.append(f"Thought {iteration}: {thought}")

        action_prompt = f"""
Based on the thought: "{thought}"
Formulate a query to retrieve missing contextual details from the document.
"""
        action = call_llm(action_prompt)
        print(f"Action Prompt: {action_prompt}\nAction Response: {action}")
        reasoning_steps.append(f"Action {iteration}: {action}")

        retrieval_prompt = f"""
Answer the following query using the provided context:
Query: "{action}"
Context: "{document_text}"
"""
        retrieved_context = call_llm(retrieval_prompt)
        print(f"Retrieval Prompt: {retrieval_prompt}\nRetrieved Context: {retrieved_context}")
        reasoning_steps.append(f"Retrieved {iteration}: {retrieved_context}")

        relevancy_score, detailed_scores = evaluate_context_quality(retrieved_context, validation_instruction)
        print(f"Score Breakdown: {detailed_scores}")

        if relevancy_score >= RELEVANCY_THRESHOLD:
            context += "\n" + retrieved_context
            break
        else:
            context += "\n" + retrieved_context
            time.sleep(1)

    final_prompt = f"""
Based on the final observations and retrieved context, generate a structured validation report.
Validation Assessment: {validation_instruction}
Context: {context}
Provide a detailed and structured response.
"""
    report = call_llm(final_prompt, temperature=0.7, max_tokens=1000)
    print(f"\nFinal Report:\n{report}")
    return report, reasoning_steps

Does the following code implement properly the recommended algorithm of Reflexion?

def run_reflexion(validation_instruction, document_text):
    memory = []
    context = ""
    iteration = 0
    relevancy_score = 0

    while relevancy_score < RELEVANCY_THRESHOLD and iteration < MAX_ITERATIONS:
        iteration += 1
        print(f"\n--- Reflexion Iteration {iteration} ---")

        thought_prompt = f"""
Based on the validation instruction: "{validation_instruction}" and memory: "{' | '.join(memory)}"
What information should be retrieved or corrected?
"""
        thought = call_llm(thought_prompt)
        print(f"Thought Prompt: {thought_prompt}\nThought Response: {thought}")
        memory.append(f"Thought {iteration}: {thought}")

        action_prompt = f"""
Based on your current thought: "{thought}"
Formulate a query to retrieve relevant context from the document.
"""
        query = call_llm(action_prompt)
        print(f"Action Prompt: {action_prompt}\nAction Response: {query}")

        retrieval_prompt = f"""
Using the following query and document, retrieve relevant content:
Query: "{query}"
Document: "{document_text}"
"""
        new_context = call_llm(retrieval_prompt)
        print(f"Retrieval Prompt: {retrieval_prompt}\nRetrieved Context: {new_context}")
        memory.append(f"Context {iteration}: {new_context}")

        relevancy_score, detailed_scores = evaluate_context_quality(new_context, validation_instruction)
        print(f"Score Breakdown: {detailed_scores}")

        if relevancy_score >= RELEVANCY_THRESHOLD:
            context += "\n" + new_context
            break
        else:
            memory.append(f"Feedback: context not sufficient, score={relevancy_score}")
            context += "\n" + new_context
            time.sleep(1)

    report_prompt = f"""
Based on your memory and retrieved context, generate a validation report.
Validation Instruction: "{validation_instruction}"
Context: "{context}"
"""
    final_report = call_llm(report_prompt, temperature=0.7, max_tokens=1000)
    print(f"\nFinal Report:\n{final_report}")
    return final_report, memory
    
# updated version 

def run_reflexion(validation_instruction, document_text):
    memory = []
    context = ""
    iteration = 0
    relevancy_score = 0
    trace_log = []

    while relevancy_score < RELEVANCY_THRESHOLD and iteration < MAX_ITERATIONS:
        iteration += 1
        print(f"\n--- Reflexion Iteration {iteration} ---")

        # Step 1: Reflect on what is missing or wrong
        thought_prompt = f"""
As a validation agent, you are reflecting on your past memory to decide what is missing or what needs to be corrected in order to fulfill the following instruction.

Validation Instruction:
"{validation_instruction}"

Memory so far:
"{' | '.join(memory)}"

Reflect on what to improve or retrieve next.
"""
        thought = call_llm(thought_prompt)
        print(f"Thought Prompt:\n{thought_prompt}\nThought Response:\n{thought}")
        memory.append(f"Thought {iteration}: {thought}")
        trace_log.append({"iteration": iteration, "step": "thought", "content": thought})

        # Step 2: Use the reflection to generate a query
        action_prompt = f"""
Based on your reflection: "{thought}"
Formulate a specific query to retrieve the missing or necessary information from the document.
"""
        query = call_llm(action_prompt)
        print(f"Action Prompt:\n{action_prompt}\nAction Response:\n{query}")
        trace_log.append({"iteration": iteration, "step": "query", "content": query})

        # Step 3: Retrieve new context (simulate document search)
        retrieval_prompt = f"""
Use the following query to find relevant information in the document.

Query: "{query}"

Document:
"{document_text}"

Return the most relevant text from the document that addresses the query.
"""
        new_context = call_llm(retrieval_prompt)
        print(f"Retrieval Prompt:\n{retrieval_prompt}\nRetrieved Context:\n{new_context}")
        memory.append(f"Context {iteration}: {new_context}")
        trace_log.append({"iteration": iteration, "step": "retrieved_context", "content": new_context})

        # Step 4: Evaluate context quality
        relevancy_score, detailed_scores = evaluate_context_quality(new_context, validation_instruction)
        print(f"Score Breakdown: {json.dumps(detailed_scores, indent=2)}")
        trace_log.append({
            "iteration": iteration,
            "step": "evaluation",
            "scores": detailed_scores,
            "average_score": relevancy_score
        })

        # Step 5: Feedback loop
        if relevancy_score >= RELEVANCY_THRESHOLD:
            print("Context is sufficiently relevant. Proceeding to report generation.")
            context += "\n" + new_context
            break
        else:
            feedback = f"Feedback: Context not sufficient (score={relevancy_score:.2f}). Reflection required."
            memory.append(feedback)
            trace_log.append({"iteration": iteration, "step": "feedback", "content": feedback})
            context += "\n" + new_context
            time.sleep(1)

    # Step 6: Generate final report
    report_prompt = f"""
Using the validation instruction and the collected memory and context, write a structured and professional model validation report.

Validation Instruction:
"{validation_instruction}"

Context:
"{context}"

Memory Log:
"{' | '.join(memory)}"
"""
    final_report = call_llm(report_prompt, temperature=0.7, max_tokens=1000)
    print(f"\nFinal Report:\n{final_report}")
    trace_log.append({"step": "final_report", "content": final_report})

    return final_report, trace_log
    
    
# Example usage:
if __name__ == "__main__":
    sample_instruction = "Assess whether the model objectives align with the core model requirements."
    sample_text = """The model is designed to detect financial abuse in elderly populations. It uses supervised
machine learning with logistic regression to predict abuse likelihood based on financial transactions. Core
requirements include interpretability, fairness, performance above 85% accuracy, and compliance with
regulatory expectations."""

    print("\nRunning ReAct Strategy...")
    react_output, react_trace = run_react(sample_instruction, sample_text)

    print("\nRunning Reflexion Strategy...")
    reflexion_output, reflexion_memory = run_reflexion(sample_instruction, sample_text)
