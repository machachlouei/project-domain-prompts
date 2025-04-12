Experimental Plan: Evaluating Prompting Techniques for Instruction-Following Document Generation

Objective

The purpose of this study is to evaluate the impact of different prompting techniques on the quality of instruction-following output produced by large language models (LLMs), particularly for generating structured document content. The research aims to answer the following questions:
	•	How do prompting techniques affect LLM output quality (e.g., relevancy, completeness, specificity)?
	•	Which prompting strategies yield the most consistent and informative results?
	•	How do smaller, open-source models compare to large-scale models like GPT-4o in reasoning-heavy tasks? How does LLaMA compare with reasoning models like Qwen?

⸻

Scope and Constraints
	•	Use Case Focus: Document generation in response to instructions, inspired by typical model documentation tasks.
	•	Data: Synthetic data is used to protect sensitive or internal information. Each instruction mimics real-world model documentation prompts but contains no confidential content.

⸻

Experimental Setup

(a) Prompting Techniques (Conditions)

Each prompting technique represents a separate experimental condition, using standardized prompt templates and preprocessing for fairness.

Prompting Techniques:
	1.	Zero-Shot Prompting
	2.	Few-Shot Prompting
	3.	Zero-Shot Chain-of-Thought (CoT)
	4.	Few-Shot Chain-of-Thought (CoT)
	5.	ReAct (Reasoning + Action + Self-criticism)
	6.	Tree of Thought (ToT)

Prompt Structure:
Standardized format across techniques to ensure comparability.

Sampling Settings:
	•	Temperature: 0.3
	•	Top-p: [TBD]
	•	Max tokens: 600

⸻

(b) Models Used

External (Cloud-hosted):
	•	GPT-4o (OpenAI)

Local/Open-Source:
	•	LLaMA-based model (e.g., LLaMA 3.2 3B)
	•	Qwen 7B

Each model is tested using the same prompt setup for fairness and comparability.

⸻

Dataset and Task Description

Task Type:

Instruction-following reasoning and document generation.

Primary Dataset:

Each data point consists of:
	•	Instruction: A complex directive (e.g., “Assess whether core model requirements are aligned with model objectives”), based on SR-11 guidelines.
	•	Context: A section of a synthetic model development document, also based on SR-11 standards.

Dataset Size:
10 core instructions × 6 prompting conditions × 3 repetitions = 180 total trials.

Data Preprocessing:
	•	Same preprocessing steps applied to all samples.
	•	Normalize text for whitespace and headers.
	•	Standardize prompts with consistent variable placeholders and delimiters.

⸻

Evaluation Metrics

Primary Metrics

Evaluated using a combination of LLM-assisted scoring and human expert review:
	•	Relevancy (1–5): Does the response directly address the instruction?
	•	Completeness (1–5): Does the response include all required elements?
	•	Specificity (1–5): Does the response include document-specific evidence?

Secondary Metrics (Optional/Manual):
	•	Accuracy: Human-in-the-loop rating from expert reviewers.
	•	Error Types (optional): Hallucinations, redundancy, lack of specificity.

⸻

Procedure
	1.	Select 10 guideline instructions from different model documentation sections (e.g., model framework, inputs, outputs, implementation, monitoring).
	2.	Pair each instruction with an appropriate context derived from synthetic SR-11-compliant model development content.
	3.	Design prompt templates for each of the six prompting techniques.
	4.	Run each prompt variation three times per model.
	5.	Evaluate each output using the evaluate_output_quality() function, which produces relevance, completeness, and specificity scores along with rationales.
	6.	Log all prompts, model outputs, and evaluation scores, including justification for each score.
	7.	Analyze results across techniques:
	•	Compute average and variance for evaluation scores.
	•	Collect optional human reviewer feedback.
	•	Analyze types of model errors (hallucination, redundancy, etc.).

⸻

Experimental Design
	•	Control Condition: Zero-shot prompting (basic instruction + context).
	•	Variable Conditions: All other prompting strategies (few-shot, CoT, ReAct, ToT).
	•	Design: Within-subjects — every prompting technique is tested on the same set of tasks.
	•	Repetitions: Each prompt condition is repeated three times to assess output consistency.

⸻

Reproducibility Measures

Maintain a JSON-based logging system that tracks:
	•	All prompts, model responses, evaluation scores, and rationales.
	•	Random seeds, temperature settings, and model versions.
	•	Version control of prompt templates and scripts.
	•	Shared Git or Jupyter interface to enable collaboration and reproducibility 
