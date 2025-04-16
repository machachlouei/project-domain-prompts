import faiss
import numpy as np
import openai
import time
from sentence_transformers import SentenceTransformer
from docx import Document

# Define API Key (Use your OpenAI API key or a local LLM endpoint)
API_KEY = "your_openai_api_key"
openai.api_key = API_KEY

# Load sentence transformer for embedding
embedding_model = SentenceTransformer("BAAI/bge-base-en")

# Load and preprocess MDD (100-page DOCX)
def load_mdd(docx_path):
    """Load and split a DOCX Model Development Document (MDD) into smaller chunks."""
    doc = Document(docx_path)
    text_chunks = []
    chunk_size = 5  # Number of sentences per chunk
    current_chunk = []
    
    for para in doc.paragraphs:
        sentences = para.text.split(". ")
        for sentence in sentences:
            if len(current_chunk) >= chunk_size:
                text_chunks.append(" ".join(current_chunk))
                current_chunk = []
            current_chunk.append(sentence)
    
    if current_chunk:
        text_chunks.append(" ".join(current_chunk))
    
    return text_chunks

# Create FAISS index
def create_faiss_index(text_chunks):
    """Create FAISS index for vector search from MDD text chunks."""
    embeddings = np.array([embedding_model.encode(chunk) for chunk in text_chunks])
    d = embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(embeddings)
    return index, text_chunks

# Retrieve context dynamically
def retrieve_context(query, faiss_index, text_chunks, top_k=3):
    """Retrieve the most relevant context chunks using FAISS."""
    query_embedding = embedding_model.encode(query).reshape(1, -1)
    distances, indices = faiss_index.search(query_embedding, top_k)
    retrieved_chunks = [text_chunks[i] for i in indices[0]]
    return "\n".join(retrieved_chunks)

# Function to call OpenAI API (or a local LLM)
def call_llm(prompt, model="gpt-4", temperature=0.3):
    """LLM API Call with controlled temperature settings."""
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "system", "content": "You are an AI assisting with model validation."},
                  {"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=temperature
    )
    return response["choices"][0]["message"]["content"]

# ReAct Algorithm with RAG using FAISS
def react_validation_assessment(validation_instruction, faiss_index, text_chunks, max_iterations=3):
    """
    Implements the ReAct framework with FAISS-based retrieval.
    Dynamically refines context, retrieves additional sections, and generates reports.
    """
    context = retrieve_context(validation_instruction, faiss_index, text_chunks)
    reasoning_steps = []

    for iteration in range(max_iterations):
        print(f"Iteration {iteration + 1}...")

        # 1. Thought Generation
        thought_prompt = f"""
        Given the validation instruction: "{validation_instruction}"
        and the retrieved context: "{context}"
        What additional information is needed for a thorough assessment?
        """
        thought = call_llm(thought_prompt, temperature=0.3)
        reasoning_steps.append(f"Thought {iteration+1}: {thought}")

        # 2. Action Selection (Retrieve More Context)
        action_prompt = f"""
        Based on the thought: "{thought}"
        Formulate a query to retrieve missing contextual details from the Model Development Document.
        """
        action = call_llm(action_prompt, temperature=0.3)
        reasoning_steps.append(f"Action {iteration+1}: {action}")

        # Retrieve new context dynamically
        additional_context = retrieve_context(action, faiss_index, text_chunks)
        context += "\n" + additional_context

        # 3. Observation Collection
        observation_prompt = f"""
        Using the updated context: "{context}"
        Provide an observation regarding how core requirements align with model objectives.
        """
        observation = call_llm(observation_prompt, temperature=0.3)
        reasoning_steps.append(f"Observation {iteration+1}: {observation}")

        # Check if enough context has been retrieved
        if "sufficient" in observation.lower():
            print("Enough context retrieved. Proceeding to report generation...")
            break

        time.sleep(2)  # Prevent API rate limits

    # 4. Final Validation Report Generation
    report_prompt = f"""
    Based on the final observations and retrieved context, generate a structured validation report.
    Validation Assessment: {validation_instruction}
    Context: {context}
    Provide a detailed and structured response.
    """
    validation_report = call_llm(report_prompt, temperature=0.7)
    return validation_report, reasoning_steps

# Load MDD and create FAISS index
mdd_chunks = load_mdd("model_development_document.docx")
faiss_index, text_chunks = create_faiss_index(mdd_chunks)

# Run ReAct-based Validation Assessment with FAISS-based RAG
generated_report, reasoning_trace = react_validation_assessment(validation_instruction, faiss_index, text_chunks)

# Print the validation report
print("\nGenerated Validation Report:\n")
print(generated_report)

# Print the reasoning steps (debugging)
print("\nReAct Reasoning Trace:\n")
for step in reasoning_trace:
    print(step)

# Automated Evaluation of the Generated Report
def evaluate_report(report, context):
    """
    Uses another LLM to assess the generated report based on evaluation metrics:
    - Relevancy
    - Hallucination
    - Comprehensiveness
    - Groundedness
    """
    evaluation_prompt = f"""
    Evaluate the following validation report based on the retrieved context.
    Validation Report: "{report}"
    Context: "{context}"
    
    Provide scores from 1 to 5 for the following criteria:
    1. Relevancy (Does the report answer the validation instruction?)
    2. Hallucination (Does the report introduce incorrect or unsupported information?)
    3. Comprehensiveness (Does the report cover all key aspects?)
    4. Groundedness (Is the report supported by the retrieved context?)
    
    Format your response as:
    Relevancy: X
    Hallucination: X
    Comprehensiveness: X
    Groundedness: X
    """
    evaluation_result = call_llm(evaluation_prompt, temperature=0.3)
    return evaluation_result

# Run Evaluation
evaluation_scores = evaluate_report(generated_report, retrieve_context(validation_instruction, faiss_index, text_chunks))

# Print Evaluation Scores
print("\nEvaluation Scores:\n")
print(evaluation_scores)