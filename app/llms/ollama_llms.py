from langchain_ollama import ChatOllama

def gemma4():
    print("#"*20)
    print("Gemma4 Model")
    print("#"*20)
    print("\n\n")

    return ChatOllama(
        model="gemma4",
        temperature=0
    )