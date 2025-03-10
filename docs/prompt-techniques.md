Literature Review: Study of Prompting Techniques in Large Language Models

Abstract

Prompt engineering plays a crucial role in enhancing the performance of large language models (LLMs). This review examines seven prominent prompting techniques—Chain of Thought (CoT), Tree of Thoughts (ToT), ReAct, Role-Based Prompting, Few-Shot Learning, Zero-Shot CoT, and Self-Consistency Prompting. We analyze their strengths, limitations, and best use cases based on recent literature, particularly arXiv publications. Understanding these methods is essential for optimizing LLM outputs in complex reasoning tasks, decision-making, and automation.

⸻

1. Introduction

Prompting techniques guide LLMs to generate more contextually relevant, logical, and accurate responses. Recent research highlights various strategies to improve reasoning, factual consistency, and adaptability of models (Brown et al., 2020; Wei et al., 2022). This study provides an overview of key prompting methods and their comparative advantages.

⸻

2. Overview of Prompting Techniques

2.1 Chain of Thought (CoT)

Overview

Chain of Thought (CoT) explicitly breaks down reasoning processes into sequential steps to improve performance in tasks requiring logical reasoning and numerical computations (Wei et al., 2022).

Strengths
	•	Enhances logical reasoning and arithmetic problem-solving (Kojima et al., 2022).
	•	Reduces hallucinations by enforcing structured output generation.
	•	Outperforms traditional prompting in multi-step problem solving.

Limitations
	•	Requires large-scale models to be effective (e.g., GPT-4, PaLM-2).
	•	Performance drops significantly on shorter prompts or ambiguous tasks.
	•	Sensitive to prompt wording and ordering.

Best Use Cases
	•	Mathematical problem-solving (Nye et al., 2021).
	•	Commonsense reasoning tasks (Wei et al., 2022).
	•	Scientific question answering (Wang et al., 2023).

Key References
	•	Wei et al. (2022), Chain of Thought Prompting Elicits Reasoning in Large Language Models [arXiv:2201.11903].
	•	Kojima et al. (2022), Large Language Models are Zero-Shot Reasoners [arXiv:2205.11916].

⸻

2.2 Tree of Thoughts (ToT)

Overview

Tree of Thoughts (ToT) expands on CoT by branching out multiple reasoning paths instead of following a linear chain (Yao et al., 2023).

Strengths
	•	More adaptive and exploratory than CoT.
	•	Allows backtracking and evaluation of different reasoning paths.
	•	Improves LLM performance on complex problems with multiple solution strategies.

Limitations
	•	Computationally expensive due to multi-branch exploration.
	•	Requires an effective pruning mechanism to avoid exponential search space growth.

Best Use Cases
	•	Complex decision-making tasks (Yao et al., 2023).
	•	Strategic game playing (e.g., chess puzzles, Go).
	•	Multi-hop reasoning problems.

Key References
	•	Yao et al. (2023), Tree of Thoughts: Deliberate Problem Solving with Large Language Models [arXiv:2305.10601].

⸻

2.3 ReAct (Reasoning + Acting)

Overview

ReAct integrates reasoning and action-taking by allowing LLMs to interact with external environments while thinking step-by-step (Yao et al., 2022).

Strengths
	•	Improves contextual understanding by retrieving real-time information.
	•	Reduces hallucinations by grounding responses in external sources.
	•	Useful for dynamic tasks requiring real-world updates.

Limitations
	•	Requires API integration for real-time retrieval.
	•	Slower than static prompting as it interacts with external systems.

Best Use Cases
	•	Task automation with retrieval-based decision-making.
	•	Dynamic question answering (QA) with online sources.
	•	Real-world applications such as medical or financial predictions.

Key References
	•	Yao et al. (2022), ReAct: Synergizing Reasoning and Acting in Language Models [arXiv:2210.03629].

⸻

2.4 Role-Based Prompting

Overview

Role-based prompting assigns a specific persona or task role to the LLM (Li et al., 2023). This enhances context awareness and response consistency.

Strengths
	•	Improves domain-specific performance (e.g., legal, medical domains).
	•	Reduces bias and improves role consistency.
	•	Works well with fine-tuned LLMs.

Limitations
	•	Less flexible for multi-domain applications.
	•	Requires well-crafted role instructions to avoid misinterpretations.

Best Use Cases
	•	Legal text generation (e.g., contract analysis).
	•	Healthcare and clinical summarization.
	•	Customer support chatbots.

Key References
	•	Li et al. (2023), Enhancing Large Language Model Understanding through Role-Based Prompting [arXiv:2306.04532].

⸻

2.5 Few-Shot Learning

Overview

Few-shot learning provides examples within prompts to guide LLMs in making inferences based on contextual patterns (Brown et al., 2020).

Strengths
	•	Highly flexible across multiple tasks.
	•	Requires less data than full fine-tuning.
	•	Works well for task adaptation without retraining.

Limitations
	•	Performance varies based on prompt length and quality.
	•	Susceptible to bias if poor examples are provided.

Best Use Cases
	•	Text classification.
	•	Natural language understanding (NLU).
	•	Summarization tasks.

Key References
	•	Brown et al. (2020), Language Models are Few-Shot Learners [arXiv:2005.14165].

⸻

2.6 Zero-Shot CoT

Overview

Zero-shot CoT extends CoT reasoning capabilities without requiring few-shot examples (Kojima et al., 2022).

Strengths
	•	No need for labeled examples.
	•	Works well for generalized reasoning tasks.
	•	Cost-effective compared to fine-tuning.

Limitations
	•	Struggles with complex multi-hop reasoning.
	•	Requires careful prompt crafting.

Best Use Cases
	•	Zero-shot QA tasks.
	•	Logical and deductive reasoning.

Key References
	•	Kojima et al. (2022), Large Language Models are Zero-Shot Reasoners [arXiv:2205.11916].

⸻

2.7 Self-Consistency Prompting

Overview

Self-consistency prompting generates multiple responses and selects the most frequent or confident one (Wang et al., 2023).

Strengths
	•	Improves robustness of responses.
	•	Works well with stochastic models.

Limitations
	•	Computationally expensive.
	•	Requires multiple forward passes.

Best Use Cases
	•	Mathematical proof validation.
	•	Fact-based QA with high reliability.

Key References
	•	Wang et al. (2023), Self-Consistency Improves Chain of Thought Reasoning in Language Models [arXiv:2203.11171].

⸻

3. Conclusion

Each prompting technique has unique advantages, making them suitable for different use cases. Chain of Thought (CoT) and Tree of Thoughts (ToT) enhance logical reasoning, while ReAct and Role-Based Prompting improve contextual awareness. Few-Shot and Zero-Shot learning offer flexibility, whereas Self-Consistency enhances reliability. Future work should explore hybrid techniques that combine these strengths.

⸻

References
	1.	Wei et al. (2022). Chain of Thought Prompting Elicits Reasoning in Large Language Models [arXiv:2201.11903].
	2.	Yao et al. (2023). Tree of Thoughts: Deliberate Problem Solving with Large Language Models [arXiv:2305.10601].
	3.	Yao et al. (2022). ReAct: Synergizing Reasoning and Acting in Language Models [arXiv:2210.03629].
	4.	Li et al. (2023). Enhancing Large Language Model Understanding through Role-Based Prompting [arXiv:2306.04532].
	5.	Brown et al. (2020). Language Models are Few-Shot Learners [arXiv:2005.14165].
	6.	Wang et al. (2023). Self-Consistency Improves Chain of Thought Reasoning in Language Models [arXiv:2203.11171].