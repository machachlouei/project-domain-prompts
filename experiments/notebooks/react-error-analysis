The ReAct paper conducts error analysis through manual annotation of model-generated trajectories, focusing particularly on the HotpotQA task. This analysis is detailed in Section 3.3 and Appendix E.1.

⸻

How the Error Analysis Was Conducted
	1.	Sampling:
	•	The authors randomly selected 50 trajectories from each of:
	•	ReAct-correct
	•	ReAct-incorrect
	•	CoT-correct
	•	CoT-incorrect
	•	Total: 200 examples
	2.	Human Annotation:
	•	Annotators categorized success and failure modes by reading full model trajectories, including:
	•	Thoughts
	•	Actions
	•	Observations
	•	Final answers
	3.	Categories Used in the Analysis:
A. Success Modes
	•	True Positive: Reasoning and facts are correct
	•	False Positive: Answer is right, but reasoning or facts are hallucinated
B. Failure Modes
	•	Reasoning Error: Logical flaw in the model’s thought process (including loops or missteps)
	•	Search Result Error (ReAct only): Retrieved content was unhelpful or empty
	•	Hallucination: Model invented incorrect facts (CoT mostly)
	•	Label Ambiguity: Prediction is arguably right, but mismatches label
	4.	Findings (from Table 2):

Error Type	ReAct	CoT
False Positive	6%	14%
Reasoning Error	47%	16%
Search Result Error	23%	—
Hallucination	0%	56%
Label Ambiguity	29%	28%

Insights:
	•	ReAct is more grounded and has fewer hallucinations.
	•	CoT is more structured, but more prone to fact errors.
	•	ReAct suffers from looping behavior and non-informative search results, which are less common in CoT.

⸻

Conclusion

The error analysis in the ReAct paper is:
	•	Manual, thorough, and qualitative + quantitative.
	•	Designed to highlight differences in behavior and failure characteristics between ReAct and CoT prompting.
	•	Used to support the claim that ReAct reduces hallucination but introduces new challenges like search reliance and repetition loops.

Here’s a visual-style table template you can use to replicate the ReAct-style error analysis on your own model outputs. It follows the structure used in Table 2 of the ReAct paper:

⸻

ReAct Error Analysis Template

Category	Definition	% of Cases	Example Notes
True Positive	Correct answer and correct, grounded reasoning	e.g., 94%	“Accurate search and correct final synthesis.”
False Positive	Correct answer but with hallucinated or logically flawed reasoning	e.g., 6%	“Final answer is right, but invented fact used.”
Reasoning Error	Incorrect answer due to flawed reasoning logic or repetitive thoughts	e.g., 47%	“Looped between irrelevant searches.”
Search Error	Incorrect answer due to unhelpful or empty search results (ReAct only)	e.g., 23%	“Search returns unrelated wiki paragraphs.”
Hallucination	Answer and/or reasoning contains facts not present in retrieved evidence	e.g., 0%	“Claimed city of birth that was never mentioned.”
Label Ambiguity	Reasonable answer that mismatches dataset label due to edge-case interpretation	e.g., 29%	“Said ‘Israeli’ vs. label ‘Israeli-American’.”



⸻

Steps to Use the Template
	1.	Sample: Choose a mix of correct and incorrect trajectories (e.g., 50 of each for ReAct and CoT).
	2.	Annotate:
	•	For each trajectory, determine which category it falls into.
	•	Fill in example notes.
	3.	Compute %: Count the number of times each category occurs and calculate percentage over total.

⸻

