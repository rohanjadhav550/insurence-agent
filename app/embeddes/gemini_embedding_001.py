from app.comman.loaders import docling_loader
from app.comman.text_splitters import text_splitter
from app.vectors.pinecone_vector_db import vecotor
from app.embedders.google_genai_embedders import gemini_embedding_001
import os

def gemini_embedder_001(document):
    # Loading the document using docling loader
    docs = docling_loader(document)

    # Splitting the documents using charcter splitter
    texts = text_splitter(docs)
    # Embedding the content
    vecotor(texts, gemini_embedding_001, os.environ["INDEX_NAME_GEMINI_001"])

# gemini_embedder_001(["/media/rohan/D-Drive/Agentic development/insurence-agent/docs/Sample-Policy-Document_LIC-s-New-Jeevan-Shanti_UIN-512N338V01-(1).pdf"])