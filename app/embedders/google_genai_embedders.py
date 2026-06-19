from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
load_dotenv()

def gemini_embedding_001():
    print("#"*20)
    print("GEMINI_EMBEDDING_001")
    print("#"*20)
    print("/n/n")
    
    return GoogleGenerativeAIEmbeddings(
        model="gemini_embedding_001"
    )

