# Customized ReAct Algorithm for Model Validation Assessment Prompting Experiment

This adaptation of the ReAct framework is tailored to test different prompting strategies (Chain of Thought, Tree of Thought, etc.) for generating validation reports based on model validation assessment instructions and contextual information extracted from model development documents (MDDs). Since no human-written reference texts are available as true labels, we will use an LLM-based evaluator to assess the quality of the generated reports.

---

## Customized ReAct Algorithm for Model Validation Assessment

### 1. Input Processing
- Given a model validation assessment instruction (e.g., *“Assess whether core requirements align with model objectives”*).
- Retrieve contextual information (e.g., relevant sections from the Model Development Document (MDD), prior validation reports, risk assessment files).
- Select a prompting strategy to test (e.g., Chain of Thought, Tree of Thought, ReAct).

### 2. Thought Generation
- The LLM generates an initial reasoning step, breaking down the validation instruction.
- It determines what additional contextual details might be needed (e.g., model objectives, segmentation variables, stress testing methodology).
- **Example Thought:**  
  *“To evaluate alignment between core requirements and objectives, I need to compare section 1.2 (Model Use) of the MDD with the stated core requirements in section 2.1 (Business Requirements).”*

### 3. Action Selection
- The LLM queries the RAG (Retrieval-Augmented Generation) system to extract additional contextual information from relevant documents.
- If necessary, it paraphrases or reformulates the query to fetch better results.
- **Example Action:**  
  *“Retrieve the ‘Model Use’ and ‘Business Requirements’ sections from the MDD for comparison.”*

### 4. Observation Collection
- The retrieved information is returned as observations.
- The LLM refines its reasoning based on these new observations.
- **Example Observation:**  
  *“The model objective states that it should generalize well across different customer segments, but the core requirement document lacks explicit mention of segmentation validation.”*

### 5. Iteration & Feedback Loop
- If the reasoning process identifies missing context, the LLM refines its query and fetches additional information.
- If enough information is gathered, the LLM proceeds to report generation.
- This iterative loop continues until a stopping criterion is met (e.g., a confidence threshold in the response is reached).

### 6. Final Validation Report Generation
- The LLM generates a structured validation report applying the selected prompting strategy (CoT, ToT, ReAct, etc.).
- **Example Output:**

  **Validation Assessment:** Core requirements alignment with model objectives.  
  **Findings:**
  - Model objective emphasizes generalization across segments.
  - Core requirements document lacks explicit mention of segmentation validation.
  - **Suggestion:** Include explicit validation tests for segmentation robustness.

---

## Automated Evaluation Using Another LLM

Since no human-written reference text exists, an evaluator LLM is used to assess the quality of the generated validation report.

### 7. LLM-based Evaluation
- The generated validation report is passed to another LLM (**Evaluator LLM**).
- The **Evaluator LLM** scores the report based on:
  - **Relevancy** (*Does the generated text answer the validation instruction?*)
  - **Hallucination** (*Does the response introduce incorrect or unsupported information?*)
  - **Comprehensiveness** (*Does the response cover all key aspects of the instruction?*)
  - **Groundedness** (*Is the response based on retrieved context?*)
- **Example Prompt for Evaluator LLM:**

Evaluate the following validation report using the criteria:
	1.	Relevancy (1-5)
	2.	Hallucination (1-5, lower is better)
	3.	Comprehensiveness (1-5)
	4.	Groundedness (1-5)

Validation Report:
[Generated Text]

Context Used:
[Retrieved Context]

- The Evaluator LLM returns a **scorecard** for the generated report.

### 8. Iterative Optimization of Prompting Strategies
- If evaluation scores are low, modify the prompting strategy:
- **If low groundedness**, improve retrieval.
- **If high hallucination**, refine instructions to constrain generation.
- **If low relevancy**, improve prompt specificity.
- Repeat the **ReAct process** with a refined prompting strategy.
- Store comparative results for different prompting techniques.

---

## Final Outcome
- Identify the most effective prompting technique for validation report generation.
- Use an LLM-based evaluation loop to refine prompts iteratively.
- Optimize report quality without relying on human-written true labels.

---

## Why This Approach Works?

✅ **ReAct enables dynamic retrieval of necessary context**  
✅ **LLM-based evaluation replaces human ground truth assessment**  
✅ **Iterative improvement ensures the best prompting technique is found**  
✅ **Automated scoring helps refine LLM generations efficiently**  

---

This customized **ReAct** implementation allows **iterative evaluation and adaptation**, ensuring that the best prompting strategy is used for **model validation assessment**.