from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

def gemma426b():
    return ChatGoogleGenerativeAI(
        model="gemma-4-31b-it",
        temperature=0,
        thinking_level="high",   # Gemma 4 only supports "minimal" or "high"
        include_thoughts=True,   # this one's fine as-is
    )