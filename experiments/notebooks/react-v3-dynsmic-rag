import openai
import time
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Define API Key (Use your OpenAI API key or a local LLM endpoint)
API_KEY = "your_openai_api_key"
openai.api_key = API_KEY

# Load embedding model for FAISS vector search
embedding_model = SentenceTransformer("BAAI/bge-base-en")

# Threshold for stopping the ReAct loop (Relevancy score should reach this)
RELEVANCY_THRESHOLD = 4.0  

# Load and preprocess MDD document
def load_mdd(file_path):
    """Simulate loading and splitting MDD document into chunks."""
    with open(file_path, "r") as f:
        text = f.read()
    sentences = text.split(". ")
    text_chunks = [" ".join(sentences[i:i+5]) for i in range(0, len(sentences), 5)]
    return text_chunks

# Create FAISS Index for dynamic retrieval
def create_faiss_index(text_chunks):
    """Create FAISS index for vector search from MDD text chunks."""
    embeddings = np.array([embedding_model.encode(chunk) for chunk in text_chunks])
    d = embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(embeddings)
    return index, text_chunks

# Retrieve most relevant context dynamically
def retrieve_context(query, faiss_index, text_chunks, top_k=3):
    """Retrieve the most relevant context chunks using FAISS."""
    query_embedding = embedding_model.encode(query).reshape(1, -1)
    distances, indices = faiss_index.search(query_embedding, top_k)
    retrieved_chunks = [text_chunks[i] for i in indices[0]]
    return "\n".join(retrieved_chunks)

# Function to call LLM
def call_llm(prompt, temperature=0.5):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an AI assisting with model validation."},
                  {"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=temperature
    )
    return response["choices"][0]["message"]["content"]

# Evaluate retrieved context before adding to loop
def evaluate_context_quality(context, validation_instruction):
    """Evaluate the relevancy of retrieved context before adding it."""
    evaluation_prompt = f"""
    Given the validation instruction: "{validation_instruction}"
    and retrieved context: "{context}"
    
    Assign a relevancy score (1 to 5) based on how useful this context is for answering the validation instruction.
    
    Format: Relevancy Score: X
    """
    evaluation_result = call_llm(evaluation_prompt, temperature=0.3)
    try:
        relevancy_score = float(evaluation_result.split(":")[-1].strip())
        return relevancy_score
    except:
        return 0  # If parsing fails, assume lowest relevancy

# ReAct Algorithm Implementation
def react_validation_assessment(validation_instruction, faiss_index, text_chunks):
    """
    Implements the ReAct framework for validation assessment.
    Iterates dynamically until relevancy threshold is reached.
    """
    reasoning_steps = []
    context = ""  # Start with an empty context
    iteration = 0
    relevancy_score = 0  # Initialize relevancy score
    
    while relevancy_score < RELEVANCY_THRESHOLD:
        iteration += 1
        print(f"Iteration {iteration}...")

        # 1. Thought Generation
        thought_prompt = f"""
        Given the validation instruction: "{validation_instruction}"
        and the retrieved context: "{context}"
        What additional information is needed for a thorough assessment?
        """
        thought = call_llm(thought_prompt, temperature=0.3)
        reasoning_steps.append(f"Thought {iteration}: {thought}")

        # 2. Action Selection (Retrieve More Context)
        action_prompt = f"""
        Based on the thought: "{thought}"
        Formulate a query to retrieve missing contextual details from the Model Development Document.
        """
        action = call_llm(action_prompt, temperature=0.3)
        reasoning_steps.append(f"Action {iteration}: {action}")

        # Retrieve new context dynamically
        additional_context = retrieve_context(action, faiss_index, text_chunks)

        # 3. Evaluate Retrieved Context Quality
        relevancy_score = evaluate_context_quality(additional_context, validation_instruction)
        print(f"Retrieved Context Relevancy Score: {relevancy_score}")

        if relevancy_score >= RELEVANCY_THRESHOLD:
            print("Sufficient relevant context retrieved. Proceeding to report generation...")
            context += "\n" + additional_context  # Append final high-relevancy context
            break
        else:
            print("Context not relevant enough, refining search...")
            context += "\n" + additional_context  # Append and continue iteration

        time.sleep(2)  # Avoid API rate limits

    # 4. Final Validation Report Generation
    report_prompt = f"""
    Based on the final observations and retrieved context, generate a structured validation report.
    Validation Assessment: {validation_instruction}
    Context: {context}
    Provide a detailed and structured response.
    """
    validation_report = call_llm(report_prompt, temperature=0.7)
    return validation_report, reasoning_steps

# Load MDD document (replace with actual document path)
mdd_file_path = "mdd_document.txt"
text_chunks = load_mdd(mdd_file_path)

# Create FAISS index
faiss_index, text_chunks = create_faiss_index(text_chunks)

# Predefined validation instruction
validation_instruction = "Assess whether core requirements align with model objectives."

# Run ReAct-based Validation Assessment with Dynamic Retrieval
generated_report, reasoning_trace = react_validation_assessment(validation_instruction, faiss_index, text_chunks)

# Print the validation report
print("\nGenerated Validation Report:\n")
print(generated_report)

# Print the reasoning steps (debugging)
print("\nReAct Reasoning Trace:\n")
for step in reasoning_trace:
    print(step)