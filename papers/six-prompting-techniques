Based on Figure 6.1 of The Prompt Report, the six prompting techniques are:
	1.	Zero-Shot (ZS)
	2.	Few-Shot (FS)
	3.	Chain-of-Thought (CoT)
	4.	Few-Shot Chain-of-Thought (FS-CoT)
	5.	Self-Consistency (SC)
	6.	Few-Shot Chain-of-Thought with Self-Consistency (FS-CoT+SC)

Here’s a brief definition and example for each:

⸻

1. Zero-Shot (ZS)

Definition: The model is given a task without any examples—only the instruction or question.

Example:

Translate the following English sentence to French: "Good morning."

Model Output:

"Bonjour."



⸻

2. Few-Shot (FS)

Definition: The model is provided with a few input-output examples before the target prompt to guide its response. ￼

Example:

English: Hello → French: Bonjour
English: Thank you → French: Merci
English: Good night → French:

Model Output:

"Bonne nuit."



⸻

3. Chain-of-Thought (CoT)

Definition: The model is prompted to generate intermediate reasoning steps leading to the final answer, enhancing performance on complex tasks.

Example:

Q: A farmer has 5 apples. He gives away 2 and then buys 3 more. How many apples does he have now?
A: He starts with 5 apples and gives away 2, leaving him with 3. Then he buys 3 more, so 3 + 3 = 6.
Answer: 6



⸻

4. Few-Shot Chain-of-Thought (FS-CoT)

Definition: Combines few-shot learning with chain-of-thought reasoning by providing examples that include both the task and the reasoning process.

Example:

Q: If a train travels 100 miles in 2 hours, what is its average speed?
A: The train travels 100 miles in 2 hours. Speed is calculated as distance divided by time. So, 100 miles / 2 hours = 50 miles per hour.
Answer: 50 mph

Q: A car travels 150 miles in 3 hours. What is its average speed?
A: The car travels 150 miles in 3 hours. Speed is distance divided by time. So, 150 miles / 3 hours = 50 miles per hour.
Answer:

Model Output:

"50 mph"



⸻

5. Self-Consistency (SC)

Definition: The model generates multiple reasoning paths for the same problem and selects the most consistent answer among them, improving reliability.

Example Process:
	•	Prompt: Same as in CoT or FS-CoT.
	•	Model generates multiple answers:
	•	Attempt 1: Answer is 6.
	•	Attempt 2: Answer is 6. ￼
	•	Attempt 3: Answer is 5.
	•	Final Answer:

"6" (most consistent answer)



⸻

6. Few-Shot Chain-of-Thought with Self-Consistency (FS-CoT+SC)

Definition: Combines FS-CoT with self-consistency by providing few-shot examples with reasoning and sampling multiple outputs to select the most consistent answer.

Example:

Q: If a car travels 60 miles in 1.5 hours, what is its average speed?
A: The car travels 60 miles in 1.5 hours. Speed is distance divided by time. So, 60 miles / 1.5 hours = 40 miles per hour.
Answer: 40 mph

Q: A cyclist covers 30 miles in 2 hours. What is their average speed?
A: The cyclist travels 30 miles in 2 hours. Speed is distance divided by time. So, 30 miles / 2 hours = 15 miles per hour.
Answer:

[Multiple model outputs are generated, and the most consistent answer is selected.]

Model Output:

"15 mph"



⸻

These techniques are designed to enhance the performance of language models on various tasks by structuring prompts to guide the model’s reasoning and output.