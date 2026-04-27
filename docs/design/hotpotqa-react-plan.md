
1. Modified Plan

We’ll:
	•	Use LangChain’s AgentExecutor with intermediate_steps logging.
	•	Return each step with:
	•	Thought (LLM’s reasoning),
	•	Action (tool selected),
	•	Action Input (what it looked up),
	•	Observation (tool response).

⸻

2. Full Python Code with ReAct Logging

from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from langchain.llms import OpenAI
from langchain.agents.agent import AgentExecutor
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.schema import AgentAction, AgentFinish
from datasets import load_dataset

# Load a small HotpotQA sample
dataset = load_dataset("hotpot_qa", "distractor", split="validation[:1]")

# Create a lookup tool that returns Wikipedia text by title
def lookup_tool(title: str, context_dict):
    for page in context_dict:
        if page[0].lower() == title.lower():
            return " ".join(page[1])
    return "Title not found."

# Function to create LangChain tool
def create_tools(context_dict):
    return [
        Tool(
            name="Lookup",
            func=lambda x: lookup_tool(x, context_dict),
            description="Useful for looking up content from a Wikipedia article title."
        )
    ]

# Run agent with intermediate step tracking
def run_react_with_logging(sample):
    question = sample["question"]
    context_dict = sample["context"]
    tools = create_tools(context_dict)
    llm = OpenAI(temperature=0, model_name="gpt-4")

    # Initialize the ReAct-style agent
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        return_intermediate_steps=True
    )

    result = agent({"input": question})
    
    # Extract Thought/Action/Observation chains
    steps = []
    for step in result["intermediate_steps"]:
        action: AgentAction = step[0]
        observation = step[1]
        steps.append({
            "thought": action.log.strip(),
            "action": action.tool,
            "action_input": action.tool_input,
            "observation": observation
        })

    return {
        "question": question,
        "answer": result["output"],
        "gold_answer": sample["answer"],
        "steps": steps
    }

# Run on one sample
output = run_react_with_logging(dataset[0])

# Display
print("QUESTION:", output["question"])
print("\nREASONING STEPS:")
for i, step in enumerate(output["steps"]):
    print(f"\nStep {i+1}")
    print("Thought:", step["thought"])
    print("Action:", step["action"])
    print("Action Input:", step["action_input"])
    print("Observation:", step["observation"])

print("\nFINAL ANSWER:", output["answer"])
print("GOLD ANSWER:", output["gold_answer"])



⸻

3. What You’ll See in Output

You’ll get step-by-step reasoning like:

Step 1
Thought: I need to find out who wrote 'A Brief History of Time'.
Action: Lookup
Action Input: A Brief History of Time
Observation: The book was written by Stephen Hawking.

Step 2
Thought: Now I need to find where Stephen Hawking was born.
Action: Lookup
Action Input: Stephen Hawking
Observation: He was born in Oxford, England.



⸻

4. Bonus Tip

You can save this trace for analysis, training, or prompting new models with real agent thought processes.

Would you like to visualize the ReAct reasoning chain as a graph (e.g., with networkx or Graphviz)?