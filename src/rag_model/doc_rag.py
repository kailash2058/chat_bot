import numpy as np
import pandas as pd
import json
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import chromadb
from .input_handler import extract
import os
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import re

# Load environment variables from the .env file
load_dotenv()

# Get the API key
google_api_key = os.getenv("GOOGLE_API_KEY")
# Initialize the Gemini API client

if google_api_key:
    print("Google API key loaded successfully.")
else:
    print("Failed to load Google API key. Make sure it's in the .env file.")

genai.configure(api_key=google_api_key)

json_filename = '../outputs/chunk_data.json'
path="../docs/constitution_main_feature.pdf" 



# Dividing into Chunks

def chunk_text_dynamic(text, max_length=300):
    import re
    sentences = re.split(r'(?<=[.!?]) +', text)  # Split by sentence
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_length:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    # print(chunks)
    return chunks

# saving chunks to json

def save_chunks_to_json(chunks, json_filename):
    data = {'chunks': []}
    
    for idx, chunk in enumerate(chunks):
        data['chunks'].append({
            'id': idx,
            'chunk': chunk
        })
    
    with open(json_filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    
    # print(f"Chunks saved to {json_filename}")


# Generating vector embeddings for the text chunks

     # Initialize the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embeddings(chunks):
    # Generate embeddings for each chunk of text
    embeddings = model.encode(chunks)
    return embeddings


# Index  Embeddings in ChromaDB



# Step 1: Initialize the new Chroma PersistentClient
client = chromadb.PersistentClient(path="../db/")  # Specify the directory to persist the database

# Step 2: Create or get a collection
collection = client.get_or_create_collection(name="rag_chunks")

# Step 3: Add chunks and embeddings to ChromaDB
def add_chunks_to_chromadb(chunks, embeddings):
    """
    Add chunked text and embeddings to ChromaDB.
    """
    # Ensure embeddings are in list format
    embeddings = [embedding.tolist() if not isinstance(embedding, list) else embedding for embedding in embeddings]

    # Create document metadata
    documents = [{"id": f"chunk-{i}", "text": chunk} for i, chunk in enumerate(chunks)]

    # Add data to the collection
    collection.add(
        documents=[doc["text"] for doc in documents],
        metadatas=[{"id": doc["id"]} for doc in documents],  # Store metadata (optional)
        ids=[doc["id"] for doc in documents],
        embeddings=embeddings
    )







def query_chromadb(query, model, collection, document_summary, top_k=2, relevance_threshold=0.15):
    """
    Query the ChromaDB collection for top-k relevant chunks with a query relevance check.
    """
# sanitizing the query to some extent for preventing from SQL attacks
    query = re.sub(r'[^a-zA-Z0-9\s]', '', query)



    # Get the query embedding using your embedding model
   #Step 1: Check query relevance
    query_embedding = model.encode([query])[0]
    summary_embedding = model.encode([document_summary])[0]

    similarity = cosine_similarity([query_embedding], [summary_embedding])[0][0]
    print("similarity score is :", similarity)
    # Step 2: Check if similarity meets the threshold
    if similarity < relevance_threshold:
        print("“Enter relevant query to the document provided.”")
        return False

    else:
        # Step 3: Perform retrieval if relevant
        results = collection.query(
            query_embeddings=[query_embedding.tolist()],  # Ensure embedding is a list
            n_results=top_k
        )

        # Step 4: Check if any results were retrieved
        if not results or not results["documents"]:
            return "No relevant chunks found for the query."

        # Retrieve relevant chunks
        relevant_chunks = results["documents"]
        return relevant_chunks

def format_retrieved_chunks(chunks):
    """
    Format the retrieved text chunks into a clear, structured format for prompt generation.
    - Chunks are numbered and separated by new lines for clarity.
    - Each chunk will be prefixed with 'Chunk X' where X is the chunk number.
    
    """
    formatted_chunks = ""
    for i, chunk in enumerate(chunks):
        formatted_chunks += f"Chunk {i + 1}:\n{chunk}\n\n"
    
    return formatted_chunks.strip()  # Clean up any extra whitespace
