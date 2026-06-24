from app.comman.loaders import docling_loader
from app.comman.text_splitters import text_splitter
from app.embedders.ollama_embedders import qwen3_embedding_latest
from app.vectors.pinecone_vector_db import vecotor
import os
from pathlib import Path

def qwen3(document):
    doc = docling_loader(document)

    text = text_splitter(doc)

    vecotor(text, qwen3_embedding_latest, os.environ["INDEX_NAME_OLLAMA"])
    

# docs_dir = Path("docs/Insurance_documents").resolve()

# for file_path in docs_dir.rglob("*.pdf"):
#     print("\n")
#     print("#"*40)
#     print("\n")
#     print(file_path)
#     print("\n")
#     print("#"*40)
#     qwen3(file_path)