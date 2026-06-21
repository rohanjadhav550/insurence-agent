from app.rags.insurence_chat import insurence_chat_ollama

def main():
    question = "Find the Policy number in LIC new jeevan shanti policy."
    insurence_chat_ollama(question)

if __name__ == "__main__":
    main()