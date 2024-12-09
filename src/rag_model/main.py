
from .doc_rag import *
# import google.generativeai as genai
from .doc_rag import format_retrieved_chunks
from .input_handler import extract

# # Example query
def doc_handler():
    path="../docs/constitution_main_feature.pdf" 

    text= extract(path)
    chunks = chunk_text_dynamic(text, max_length=300)
    save_chunks_to_json(chunks,json_filename)
    embeddings = generate_embeddings(chunks)
    # Step 1: Initialize the new Chroma PersistentClient
    client = chromadb.PersistentClient(path="../db/")  # Specify the directory to persist the database

    # Step 2: Create or get a collection
    collection = client.get_or_create_collection(name="rag_chunks")

    # Step 3: Add chunks and embeddings to ChromaDB
    add_chunks_to_chromadb(chunks, embeddings)

