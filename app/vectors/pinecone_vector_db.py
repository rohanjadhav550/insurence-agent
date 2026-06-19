from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
from app.embedders.google_genai_embedders import gemini_embedding_001
import os
load_dotenv()

def vecotor(text):
    print("#"*20)
    print("Embedding Master")
    print("#"*20)
    print("/n/n")

    print("INITIATING EMBEDDER....")
    print("/n/n")
    embedder = gemini_embedding_001()

    print("EMBEDDING STARTED...")
    print("/n/n")
    PineconeVectorStore.from_documents(text, embedding=embedder, index_name=os.environ["INDEX_NAME"])
    print("EMBEDDING COMPLETED!!")
    print("#"*20)
    print("/n/n")
