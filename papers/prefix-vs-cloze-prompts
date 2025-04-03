The Prompt Report discusses prefix and cloze prompts as two foundational prompt structures. Here’s a breakdown with clear examples:

⸻

1. Prefix Prompts

Definition:
Prefix prompts provide context, instructions, or examples before asking the model to generate a continuation. The model’s task is to complete the prompt based on what came before.

Structure:

[Prefix] → [Model generates continuation]

Examples:
	•	Instructional Prefix Prompt:
“Summarize the following paragraph:
’The Industrial Revolution began in the 18th century and…’”
→ (Model generates a summary.)
	•	Few-Shot Prefix Prompt:
“English: Hello → Spanish: Hola
English: Thank you → Spanish: Gracias
English: Good night → Spanish:”
→ (Model completes with “Buenas noches”)
	•	Story Prefix Prompt:
“Once upon a time, in a forest filled with glowing trees, a young fox named Fira…”
→ (Model continues the story.)

⸻

2. Cloze Prompts

Definition:
Cloze prompts contain a blank or missing element (often denoted by a token like ____, [MASK], or similar). The model is asked to fill in the missing piece — this is typical in masked language modeling tasks.

Structure:

[Context with blank] → [Model fills in the blank]

Examples:
	•	Simple Cloze Prompt:
“Paris is the capital of ____.”
→ (Expected: “France”)
	•	Masked Cloze Prompt (BERT-style):
“The cat sat on the [MASK].”
→ (Expected: “mat”)
	•	Knowledge Cloze Prompt:
“The chemical symbol for water is ____.”
→ (Expected: “H2O”)

⸻

Summary

Type	Structure	Model Action	Example
Prefix	Starts with input or instructions	Continues text	“Translate: Hello →” → “Hola”
Cloze	Has a blank/mask in the sentence	Fills in the blank	“The capital of Japan is ____.” → “Tokyo”

