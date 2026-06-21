from app.embedders.google_genai_embedders import gemini_embedding_001
from app.embedders.ollama_embedders import qwen3_embedding_latest
from langchain.tools import tool
from langchain_pinecone import PineconeVectorStore
import os
from typing import AsyncGenerator

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

    retriver = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 6, "lambda_mult": 0.25})

    return retriver.invoke(question)

@tool
def scanner_qwen3_embed(question):
    """
    This tool is ment to scan the insurence policy mentioned by the user. Following are the aspects that this tool do
        1. This will fetch the vectors by doing similarity search.
    Inputs: 
        question: user question to which we have to answer
    """
    
    print(f"QUESTION: {question}")

    vector_store = PineconeVectorStore(
        index_name=os.environ["INDEX_NAME_OLLAMA"],
        embedding=qwen3_embedding_latest()
    )

    retriver = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 6, "lambda_mult": 0.25})
    
    return retriver.invoke(question)




