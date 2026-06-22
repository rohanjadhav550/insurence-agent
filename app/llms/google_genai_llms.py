from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

def gemma426b():
    return ChatGoogleGenerativeAI(
        model="gemma-4-31b-it",
        temperature=0
    )