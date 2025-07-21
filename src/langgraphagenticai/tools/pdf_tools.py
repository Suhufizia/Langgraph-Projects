from pypdf import PdfReader
from langchain_community.tools.tavily_search import TavilySearchResults

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

def get_tools(tavily_api_key=None):
    tools = []
    if tavily_api_key:
        tools.append(TavilySearchResults(max_results=2, tavily_api_key=tavily_api_key))
    return tools