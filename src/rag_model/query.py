
from .doc_rag import *
import google.generativeai as genai
from .doc_rag import format_retrieved_chunks
from .main import doc_handler
gen_model = genai.GenerativeModel('gemini-1.5-flash')


# main()
def query_doc(query):
    text_file_path= "../outputs/extracted_text.txt"

    with open(text_file_path, "r", encoding="utf-8") as f:
        document_summary = f.read()

    # doc_handler()    #-----------> uncomment and run the code for new docs


    # query = input("Enter document related query: ")
    # retrieved_chunks = query_chromadb(query, model, collection)
    retrieved_chunks=query_chromadb(query, model, collection, document_summary,top_k=2, relevance_threshold=0.15)
    # print("##################################Retrieved Chunks:", retrieved_chunks)
    if retrieved_chunks == False:
        return " Enter relevant query to the document provided."
    else:
        formatted_chunks=format_retrieved_chunks(retrieved_chunks)
        print("##################################Retrieved Chunks:",formatted_chunks)


        # LLM for final structured result
        prompt = f"Please summarize and provide a well-organized response based on the following chunks of text:\n\n{formatted_chunks}" 
        # Send the formatted chunks to Gemini API
        response = gen_model.generate_content(prompt)
        # print (response)
        print(response.text)
        # Extract the result from the response
        return response.text
        # return retrieved_chunks