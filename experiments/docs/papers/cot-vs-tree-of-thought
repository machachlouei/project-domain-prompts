Chain of Thought (CoT) and Tree of Thought (ToT) are both prompting strategies designed to improve reasoning in language models, but they differ in how reasoning paths are structured and explored.

⸻

Chain of Thought (CoT)

Linear step-by-step reasoning. The model generates a single sequence of intermediate steps leading to the final answer.
	•	Structure:
Thought1 → Thought2 → Thought3 → Answer
	•	Goal: Mimic human-like step-by-step problem-solving
	•	Example:

Q: If a bag contains 3 red, 2 green, and 5 blue marbles, what is the probability of randomly selecting a green marble?

A: First, count the total number of marbles: 3 + 2 + 5 = 10.
There are 2 green marbles out of 10.
So, the probability is 2/10 or 1/5.
Answer: 1/5



⸻

Tree of Thought (ToT)

Branching reasoning paths. The model explores multiple possible thoughts or decisions at each step — like a decision tree — and selects the most promising path.
	•	Structure:
Thought1 →
├─ Option A → A1 → A2 → Answer
└─ Option B → B1 → B2 → Answer
	•	Goal: Explore alternative reasoning paths, evaluate them, and choose the best outcome.
	•	Example:

Q: What is the best next move in a simplified board game scenario?

Thought1: Possible moves are A and B.

Branch A:
  A1: Move A captures a piece but exposes the king.
  A2: Evaluate board position → high risk.

Branch B:
  B1: Move B defends the king and gains center control.
  B2: Evaluate board position → stable.

Choose B as the best move.
Answer: Move B



⸻

Key Differences

Feature	Chain of Thought	Tree of Thought
Reasoning structure	Linear	Branching / Exploratory
Paths explored	One	Multiple (parallel/alternative)
Evaluation	At the end	At each decision point
Strength	Good for straightforward tasks	Better for complex, multi-step tasks



⸻
