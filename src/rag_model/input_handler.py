from PyPDF2 import PdfReader



def extract(path):
    """
    Extracts text from a PDF file and stores it in a specified file.
    
    """
    output_path= "../outputs/extracted_text.txt"
    reader = PdfReader(path)
    text = ""
    
    # Extract text from each page
    for page in reader.pages:
        text += page.extract_text()
    
    # Store extracted text in a file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    
    print(f"Text successfully extracted and saved to {output_path}")
    return text
