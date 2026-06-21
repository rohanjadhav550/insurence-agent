from app.comman.loaders import docling_loader
from app.comman.text_splitters import text_splitter
from app.embedders.ollama_embedders import qwen3_embedding_latest
from app.vectors.pinecone_vector_db import vecotor
import os

def qwen3(document):
    doc = docling_loader(document)

    text = text_splitter(doc)

    vecotor(text, qwen3_embedding_latest, os.environ["INDEX_NAME_OLLAMA"])

# qwen3(["/media/rohan/D-Drive/Agentic development/insurence-agent/docs/Sample-Policy-Document_LIC-s-New-Jeevan-Shanti_UIN-512N338V01-(1).pdf"])