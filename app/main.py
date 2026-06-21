from app.rags.insurence_chat import insurence_chat_ollama

def main():
    question = "What all details are there in the HDFC Life Term Insurance policy?"
    insurence_chat_ollama(question)

if __name__ == "__main__":
    main()