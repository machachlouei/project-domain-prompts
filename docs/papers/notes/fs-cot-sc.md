The Prompt Report provides both a template and a concrete example for the Few-Shot Chain-of-Thought with Self-Consistency (FS-CoT+SC) prompting strategy.

⸻

Definition

Few-Shot Chain-of-Thought + Self-Consistency (FS-CoT+SC) combines:
	•	Few-shot chain-of-thought examples: where each training example in the prompt includes reasoning steps and a final answer.
	•	Self-consistency decoding: instead of generating a single output, the model generates multiple outputs (e.g., 5–10 completions) with different random seeds or sampling temperatures. The majority answer among the generated completions is selected as the final prediction.

This approach aims to reduce variance and boost accuracy, especially on complex reasoning tasks like those in MMLU.

⸻

Template (from the paper)

Q1: [Question 1]
A1: [Step-by-step reasoning for Q1]
Answer: [Final answer for Q1]

Q2: [Question 2]
A2: [Step-by-step reasoning for Q2]
Answer: [Final answer for Q2]

...

Qn: [New question]
An:

The model is prompted to continue the chain of thought for the new question (Qn), then this prompt is sampled multiple times (with temperature > 0), and the most common final answer is chosen.

⸻

Example (adapted from the paper)

Q: If you have 3 apples and you eat 1, how many do you have left?
A: Start with 3 apples. You eat 1 apple, so 3 - 1 = 2 apples.
Answer: 2

Q: If a bookshelf has 10 books and 4 are removed, how many remain?
A: There are 10 books initially. Removing 4 means 10 - 4 = 6 books.
Answer: 6

Q: Sarah has 15 candies. She gives 7 to her friends. How many does she have now?
A:

Then, the model is sampled multiple times with this prompt, and the most frequently occurring answer among those completions is selected.

⸻
