from langchain_ollama import ChatOllama

def gemma4():
    print("#"*20)
    print("Gemma4 Model")
    print("#"*20)
    print("\n\n")

    return ChatOllama(
        model="gemma4",
        temperature=0,
        # reasoning=True
    )
def gemma412b():
    print("#"*20)
    print("Gemma4 Model")
    print("#"*20)
    print("\n\n")

    return ChatOllama(
        model="gemma4:12b",
        temperature=0,
        reasoning=True
    )
def gemma431b():
    print("#"*20)
    print("Gemma431b Model")
    print("#"*20)
    print("\n\n")

    return ChatOllama(
        model="gemma4:31b",
        temperature=0,
        reasoning=True
    )