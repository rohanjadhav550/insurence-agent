from app.llms.google_genai_llms import gemma426b
from langchain.tools import tool

@tool
def scanner(document):
    """
    This tool is ment to scan the insurence policy mentioned by the user
    """

