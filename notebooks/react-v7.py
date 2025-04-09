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
        avg_score, scores, explanations = evaluate_context_quality(additional_context, validation_instruction)
        relevancy_score = avg_score

        print("\nContext Evaluation Scores:")
        for metric, score in scores.items():
            explanation = explanations.get(metric, "")
            print(f"{metric}: {score} — {explanation}")
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