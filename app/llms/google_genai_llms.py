from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

def gemma426b():
    return ChatGoogleGenerativeAI(
        model="gemma-4-31b-it",
        temperature=0,
        thinking_config={
            "thinking_budget": 8000,   # tokens allocated for thinking (0 to disable)
            "include_thoughts": True   # expose thought tokens in the stream
        }
    )