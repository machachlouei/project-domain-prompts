Below is an implementation template that combines ReAct and Reflexion for instruction-following document generation tasks, such as model validation report writing. This hybrid framework uses:
	•	ReAct loop: for iterative reasoning + querying.
	•	Reflexion layer: to reflect on failures and improve subsequent iterations.

⸻

Hybrid ReAct + Reflexion Implementation Template

1. Initialization

episodic_memory = []
MAX_ITERATIONS = 5
RELEVANCY_THRESHOLD = 4.0



⸻

2. ReAct + Reflexion Loop

def react_reflexion_assessment(validation_instruction, context_document):
    reasoning_trace = []
    current_context = ""
    iteration = 0
    final_report = ""
    
    while iteration < MAX_ITERATIONS:
        iteration += 1
        print(f"\n--- Iteration {iteration} ---\n")

        # ---- THOUGHT ----
        thought_prompt = f"""
        Validation Instruction: "{validation_instruction}"
        Current Context: "{current_context}"
        Memory: {episodic_memory}
        
        What additional information is needed to complete the validation?
        """
        thought = call_llm(thought_prompt)
        reasoning_trace.append(f"Thought {iteration}: {thought}")
        print(f"[Thought]: {thought}\n")

        # ---- ACTION ----
        action_prompt = f"""
        Based on the above thought, generate a specific query to retrieve relevant context.
        """
        query = call_llm(action_prompt)
        print(f"[Action]: {query}\n")

        # ---- SIMULATE CONTEXT RETRIEVAL ----
        context_prompt = f"""
        Query: "{query}"
        Document: "{context_document}"
        
        Extract the most relevant information to support the validation instruction.
        """
        additional_context = call_llm(context_prompt)
        current_context += "\n" + additional_context
        print(f"[Retrieved Context]: {additional_context[:300]}...\n")

        # ---- EVALUATION ----
        avg_score, score_details, reasoning = evaluate_context_quality(current_context, validation_instruction)
        print(f"[Evaluation Scores]: {score_details}")
        print(f"[Evaluation Reasoning]: {reasoning}\n")

        if avg_score >= RELEVANCY_THRESHOLD:
            print("Context sufficient. Proceeding to report generation.\n")
            break

        # ---- REFLEXION ----
        reflection_prompt = f"""
        Previous attempt did not meet the quality threshold.
        Instruction: "{validation_instruction}"
        Context: "{current_context}"
        Scores: {score_details}

        Reflect on what went wrong and how to do better next time.
        """
        reflection = call_llm(reflection_prompt)
        episodic_memory.append(reflection)
        print(f"[Reflection]: {reflection}\n")

    # ---- FINAL REPORT GENERATION ----
    report_prompt = f"""
    Based on the instruction and the final context, write a model validation report section.
    Instruction: "{validation_instruction}"
    Context: "{current_context}"
    """
    final_report = call_llm(report_prompt)
    return final_report, reasoning_trace, episodic_memory



⸻

3. Supporting Function (Evaluation with Reasoning)

Ensure you have evaluate_context_quality() returning reasoning as in the latest version:

def evaluate_context_quality(context, instruction):
    # Prompt LLM to evaluate context with justification (returns scores + reasoning)
    ...
    return avg_score, {"Relevancy": x, "Completeness": y, "Specificity": z}, reasoning_text



⸻

4. Run an Example

instruction = "Assess whether the core model requirements align with the model objectives."
context_document = load_mdd("mdd_doc.txt")  # or simulate one
report, trace, memory = react_reflexion_assessment(instruction, context_document)



⸻

Benefits of the Hybrid Design

Feature	Benefit
ReAct	Structured iterative reasoning with explainable steps.
Reflexion	Learns from previous missteps across iterations.
Episodic Memory	Retains helpful (or failed) strategies for adaptation.
Evaluation Loop	Enforces quality checkpoints with verbal feedback.



⸻
