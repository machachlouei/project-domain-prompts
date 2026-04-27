
⸻


# 🧠 ReAct-Based Context Validation Framework

This project implements an LLM-powered **ReAct-style validation assessment framework** for intelligently evaluating the quality of retrieved textual context in relation to a given validation instruction. The system mimics human reasoning by iteratively identifying information gaps, forming questions, retrieving data, and assessing the relevance and completeness of the content.

---

## 🚀 Purpose

The main goal is to automate **validation of model documentation** or related content using LLMs in a way that is:
- Iterative
- Structured
- Score-driven
- Human-interpretable

This is particularly useful for reviewing outputs like model development documentation, risk assessments, or audit artifacts.

---

## 🔁 Core Workflow (ReAct Loop)

The framework is based on a ReAct loop: **Reasoning → Acting → Evaluating**:

1. **Thought Generation**  
   Generate a concise thought identifying what's missing in the current context.

2. **Query Formulation**  
   Based on the thought, ask a targeted question to gather more information.

3. **Context Retrieval**  
   Simulate answering the query using source documentation.

4. **Context Evaluation**  
   Score the retrieved context on:
   - Relevancy (50% weight)
   - Completeness (30%)
   - Specificity (20%)

5. **Iteration or Completion**  
   Repeat until a high-quality context is found or max attempts are reached.

6. **Report Generation**  
   Generate a final, structured validation report based on the best available context.

---

## 📦 Modules Overview

### `evaluate_context_quality(context, validation_instruction, max_retries)`
- **Purpose**: Scores the quality of a given context using a structured LLM evaluation.
- **Returns**: 
  - Weighted average score (float)
  - Full score breakdown by metric (dict)
  - Justifications for each metric (dict)
- **Includes**:
  - JSON parsing with error handling
  - Response sanitization to strip Markdown formatting

---

### `react_validation_assessment(validation_instruction, text)`
- **Purpose**: Runs the ReAct-based loop for dynamic context discovery and evaluation.
- **Returns**:
  - Final validation report (str)
  - List of reasoning steps taken (List[str])
- **Includes**:
  - Dynamic LLM prompting for thought, query, and retrieval
  - Looping logic with early exit on score threshold

---

## 🧠 Evaluation Metrics

Each context is evaluated against three core metrics:

| Metric        | Weight | Description |
|---------------|--------|-------------|
| **Relevancy** | 50%    | Does the content directly address the instruction? |
| **Completeness** | 30% | Does it include all required elements? |
| **Specificity** | 20%  | Does it reference specific terms, metrics, or definitions? |

---

## ⚠️ Error Handling

- Markdown-style ` ```json ` formatting is stripped from LLM responses before JSON parsing.
- Fallback scores (1s) are returned if parsing fails after multiple retries.
- Detailed error logs and raw outputs are printed for transparency.

---

## 📚 Example Use Case

```python
validation_instruction = "Identify and explain the model objectives and core model requirements."
report, steps = react_validation_assessment(validation_instruction, model_document_text)
print(report)


⸻

✅ Dependencies
	•	Python 3.7+
	•	OpenAI-compatible LLM interface (e.g., call_llm())
	•	json, re, time

⸻

📌 Notes
	•	The system is LLM-agnostic but assumes a reliable JSON-formatted response.
	•	You can easily swap in your own retrieval and reasoning prompts.
	•	Extendable to many domains beyond ML documentation.

⸻

🛠 Future Improvements
	•	Cache or vector store for retrieval
	•	GUI/interactive notebook interface
	•	Multi-model ensemble evaluation
	•	Report output formatting (Markdown/PDF)

⸻




import json
import re

def evaluate_context_quality(context, validation_instruction, max_retries):
    """
    Evaluate retrieved context against a validation instruction using:
    - Relevancy (50%)
    - Completeness (30%)
    - Specificity (20%)
    Each criterion includes both a numeric score (1–5) and justification.
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
    "Justification": "Explanation..."
  }},
  "Completeness": {{
    "Score": Y,
    "Justification": "Explanation..."
  }},
  "Specificity": {{
    "Score": Z,
    "Justification": "Explanation..."
  }}
}}

Where X, Y, Z are scores from 1 (very poor) to 5 (excellent).
Do not include any commentary outside the JSON structure.
"""

    for attempt in range(max_retries):
        response = call_llm(
            evaluation_prompt,
            temperature=0.3,
            max_tokens=MAX_TOKENS,
            system_prompt=SYSTEM_PROMPT
        )

        try:
            # Remove markdown code block markers
            clean_response = re.sub(r"```(?:json)?", "", response, flags=re.IGNORECASE).strip()

            print(f"[DEBUG] Cleaned response before parsing:\n{clean_response}\n")

            scores = json.loads(clean_response)

            # Validate keys
            for metric in ["Relevancy", "Completeness", "Specificity"]:
                if metric not in scores or "Score" not in scores[metric]:
                    raise ValueError(f"Missing score for {metric}")

            avg_score = (
                scores["Relevancy"]["Score"] * 0.5 +
                scores["Completeness"]["Score"] * 0.3 +
                scores["Specificity"]["Score"] * 0.2
            )

            explanations = {
                "Relevancy": scores["Relevancy"]["Justification"],
                "Completeness": scores["Completeness"]["Justification"],
                "Specificity": scores["Specificity"]["Justification"]
            }

            return avg_score, scores, explanations

        except Exception as e:
            print(f"[Error] Attempt {attempt + 1} failed during evaluation: {e}")
            print(f"[Raw response]:\n{response}\n")

    # Fallback
    print("[Fallback] All evaluation attempts failed. Returning default low scores.")
    return 1, {
        "Relevancy": {"Score": 1, "Justification": "Parsing failed."},
        "Completeness": {"Score": 1, "Justification": "Parsing failed."},
        "Specificity": {"Score": 1, "Justification": "Parsing failed."}
    }, {
        "Relevancy": "Parsing failed.",
        "Completeness": "Parsing failed.",
        "Specificity": "Parsing failed."
    }

def react_validation_assessment(validation_instruction, text):
    reasoning_steps = []
    context = ""
    iteration = 0
    relevancy_score = 0

    while relevancy_score < RELEVANCY_THRESHOLD and iteration < MAX_ITERATIONS:
        iteration += 1
        print("\n" + "=" * 60)
        print(f"Iteration {iteration}...")

        # 1. Thought Generation
        thought_prompt = f"""
Given the validation instruction: "{validation_instruction}"
and the retrieved context: "{context}"
What additional information is needed for a thorough assessment? Provide a concise answer in one sentence.
"""
        system_prompt = "Provide a concise answer in 1–3 sentences maximum."
        thought = call_llm(thought_prompt, temperature=0.3, max_tokens=500, system_prompt=system_prompt)
        print("Generated Thought:\n", thought)
        reasoning_steps.append(f"Thought (iteration {iteration}): {thought}")

        # 2. Action Selection (Query Formulation)
        action_prompt_for_query_formulation = f"""
Based on the thought: "{thought}",
formulate a query to retrieve missing contextual details from the Model Development Document.
"""
        action_1 = call_llm(action_prompt_for_query_formulation, temperature=0.3, max_tokens=500, system_prompt=system_prompt)
        print("Generated Action (Query):\n", action_1)
        reasoning_steps.append(f"Action (iteration {iteration}) (Query Formulation): {action_1}")

        # 3. Retrieve Context (simulated)
        action_prompt_retrieve_context = f"""
Answer the query using the provided CONTEXT.
QUERY: {action_1}
CONTEXT: "{text}"
"""
        additional_context = call_llm(action_prompt_retrieve_context, temperature=0.3, max_tokens=500, system_prompt=system_prompt)
        print("Retrieved Additional Context:\n", additional_context)
        reasoning_steps.append(f"Action (iteration {iteration}) (Context Retrieved): {additional_context}")

        # 4. Evaluate Retrieved Context Quality
        avg_score, scores, explanations = evaluate_context_quality(additional_context, validation_instruction, max_retries=3)
        relevancy_score = avg_score

        print("\nContext Evaluation Scores:")
        for metric, score_obj in scores.items():
            explanation = explanations.get(metric, "")
            print(f"{metric}: {score_obj['Score']}  {explanation}")
        print(f"Average Relevancy Score: {avg_score}")

        if relevancy_score >= RELEVANCY_THRESHOLD:
            print("\nSufficient relevant context retrieved. Proceeding to report generation...")
            context += "\n" + additional_context
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
    print("Generated Validation Report:\n", validation_report)

    return validation_report, reasoning_steps
