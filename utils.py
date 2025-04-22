from google import genai
from langchain_community.document_loaders import PyPDFLoader
import ast
from pydantic import BaseModel



def ekb_search(query):
    
    client = genai.Client(api_key="")
    
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=query
    )
    return response.text

def extract_pdf(pdf_path):
    
    # Initialize loader
    loader = PyPDFLoader(pdf_path)
    
    # Load all pages
    pages = loader.load()
    
    # Combine all page contents into a single string
    full_text = "\n".join(page.page_content for page in pages)
    
    return full_text  # Print the first 500 characters for sanity check
    
def entity_extraction(content):

    class Employment(BaseModel):
        company: str
        designation: str
        compensation: float
    
    
    
    client = genai.Client(api_key="")
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=f'''Instructions:
        Given the content of the document, perform entity extraction for company, designation and gross pay.
        compensation =  gross pay before tax deductions in the salary slip * 12.
        
        Content:
        {content}''',
        config={
            'response_mime_type': 'application/json',
            'response_schema': Employment,
        },
    )
    # Use the response as a JSON string.
    print(response.text)
    
    # Use instantiated objects.
    employment: Employment = response.parsed
    return ast.literal_eval(response.text)
    
def ee_on_path(file_path):
    content_ = extract_pdf(file_path)
    employment = entity_extraction(content_)
    employment['filename'] = file_path.rsplit("/")[-1]
    return employment

