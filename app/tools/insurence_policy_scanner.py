from app.embedders.google_genai_embedders import gemini_embedding_001
from app.embedders.ollama_embedders import qwen3_embedding_latest
from langchain.tools import tool
from langchain_pinecone import PineconeVectorStore
import os

@tool
def scanner_gemini_embed(question):
    """
    This tool is ment to scan the insurence policy mentioned by the user. Following are the aspects that this tool do
        1. This will fetch the vectors by doing similarity search.
    Inputs: 
        question: user question to which we have to answer
    """

    vector_store =  PineconeVectorStore(
        index_name=os.environ["INDEX_NAME"], 
        embedding=gemini_embedding_001()
    )

    retriver = vector_store.as_retriever()

    return retriver.invoke(question)

@tool
def scanner_qwen3_embed(question):
    """
    This tool is ment to scan the insurence policy mentioned by the user. Following are the aspects that this tool do
        1. This will fetch the vectors by doing similarity search.
    Inputs: 
        question: user question to which we have to answer
    """

    vector_store = PineconeVectorStore(
        index_name=os.environ["INDEX_NAME_OLLAMA"],
        embedding=qwen3_embedding_latest()
    )

    retriver = vector_store.as_retriever()

    return retriver.invoke(question)




