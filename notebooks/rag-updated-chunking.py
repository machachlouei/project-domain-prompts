import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
import re

# Load Improved Embedding Model
embedding_model = SentenceTransformer("BAAI/bge-base-en")  # Using BGE embeddings

# Function to clean text
def clean_text(text):
    """Preprocess text by removing extra spaces and normalizing formatting."""
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    return text.strip()

# Improved Chunking Strategy: Section-based with Overlap
def load_mdd(file_path, chunk_size=512, overlap=128):
    """
    Load the MDD document and split it into section-based chunks with overlapping windows.
    
    Args:
        file_path (str): Path to the MDD document.
        chunk_size (int): Maximum token size per chunk.
        overlap (int): Overlap size between chunks.
        
    Returns:
        text_chunks (list): List of section-based overlapping chunks.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    text = clean_text(text)
    
    # Use sections (headers/subsections) as a natural boundary
    sections = re.split(r'\n\d+\.\d+\s+[A-Z][A-Za-z ]+', text)  # Detect headers like "2.1 Core Requirements"
    
    text_chunks = []
    for section in sections:
        words = section.split()
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i : i + chunk_size])
            text_chunks.append(chunk)

    return text_chunks

# Create FAISS Index for Dynamic Retrieval
def create_faiss_index(text_chunks):
    """
    Create FAISS index for vector search from MDD text chunks.
    
    Args:
        text_chunks (list): List of text chunks.
        
    Returns:
        index (faiss.IndexFlatL2): FAISS index for similarity search.
        embeddings (np.array): Array of chunk embeddings.
        text_chunks (list): List of indexed text chunks.
    """
    # Convert text chunks to embeddings
    embeddings = np.array([embedding_model.encode(chunk) for chunk in text_chunks])
    
    # Create FAISS Index
    d = embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(embeddings)
    
    return index, embeddings, text_chunks

# BM25 Keyword Search for Hybrid Retrieval
def create_bm25_index(text_chunks):
    """
    Create BM25 index to allow keyword-based search as a complement to FAISS.
    
    Args:
        text_chunks (list): List of text chunks.
        
    Returns:
        bm25 (BM25Okapi): BM25 search index.
    """
    tokenized_chunks = [chunk.split() for chunk in text_chunks]
    bm25 = BM25Okapi(tokenized_chunks)
    return bm25

# Hybrid Retrieval: FAISS + BM25
def retrieve_relevant_chunks(query, faiss_index, embeddings, text_chunks, bm25, top_k=3, bm25_weight=0.5):
    """
    Retrieve relevant MDD sections dynamically using FAISS (vector search) + BM25 (keyword search).
    
    Args:
        query (str): Search query.
        faiss_index (faiss.IndexFlatL2): FAISS index for vector retrieval.
        embeddings (np.array): FAISS embeddings.
        text_chunks (list): List of text chunks.
        bm25 (BM25Okapi): BM25 keyword search index.
        top_k (int): Number of top retrieved results.
        bm25_weight (float): Weight factor for BM25 scoring.
        
    Returns:
        retrieved_chunks (list): Top relevant text chunks.
    """
    # Get embedding for query
    query_embedding = np.array([embedding_model.encode(query)])

    # FAISS Retrieval
    _, faiss_indices = faiss_index.search(query_embedding, top_k)
    faiss_results = [text_chunks[idx] for idx in faiss_indices[0]]

    # BM25 Retrieval
    bm25_scores = bm25.get_scores(query.split())
    top_bm25_indices = np.argsort(bm25_scores)[::-1][:top_k]
    bm25_results = [text_chunks[idx] for idx in top_bm25_indices]

    # Hybrid Ranking: Combine FAISS and BM25 results
    combined_results = list(set(faiss_results + bm25_results))
    return combined_results

# Example Usage
file_path = "MDD.txt"  # Update with actual path to the MDD document
text_chunks = load_mdd(file_path)
faiss_index, embeddings, text_chunks = create_faiss_index(text_chunks)
bm25 = create_bm25_index(text_chunks)

query = "What are the core model requirements?"
retrieved_context = retrieve_relevant_chunks(query, faiss_index, embeddings, text_chunks, bm25)

print("Retrieved Context:\n", retrieved_context)