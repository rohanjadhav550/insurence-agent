from langchain_ollama import OllamaEmbeddings

def qwen3_embedding_latest():
    print("\n")
    print("#"*20)
    print("Qwen3 Embedding Model")
    print("#"*20)
    print("\n")

    return OllamaEmbeddings(
        model="qwen3-embedding"
    )