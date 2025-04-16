import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load a document from a file
def load_document(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# Split the document into chunks
def split_text(text, chunk_size=300):
    sentences = text.split(". ")
    chunks = []
    chunk = ""
    for sentence in sentences:
        if len(chunk) + len(sentence) < chunk_size:
            chunk += sentence + ". "
        else:
            chunks.append(chunk.strip())
            chunk = sentence + ". "
    if chunk:
        chunks.append(chunk.strip())
    return chunks

# Convert text chunks into vector embeddings using a transformer model
def embed_text(chunks, model):
    return np.array([model.encode(chunk) for chunk in chunks], dtype=np.float32)

# Store embeddings in FAISS for fast retrieval
def build_faiss_index(embeddings):
    d = embeddings.shape[1]  # Dimension of embeddings
    index = faiss.IndexFlatL2(d)  # L2 similarity search
    index.add(embeddings)
    return index

# Query the FAISS index for relevant document chunks
def query_document(query, index, chunks, model, top_k=3):
    query_embedding = np.array([model.encode(query)], dtype=np.float32)
    _, indices = index.search(query_embedding, top_k)  # Find top_k most similar chunks
    return [chunks[i] for i in indices[0]]

# Main Execution
if __name__ == "__main__":
    file_path = "document.txt"  # Path to your document
    model = SentenceTransformer("all-MiniLM-L6-v2")  # Load a lightweight embedding model

    # Load and process the document
    document_text = load_document(file_path)
    chunks = split_text(document_text)

    # Generate embeddings and store in FAISS
    embeddings = embed_text(chunks, model)
    faiss_index = build_faiss_index(embeddings)

    # Query the document
    query = "What are the key validation assessment instructions for the ReAct algorithm?"
    results = query_document(query, faiss_index, chunks, model)

    # Print the most relevant passages
    print("\nRelevant Passages:\n")
    for i, passage in enumerate(results):
        print(f"{i+1}. {passage}\n")