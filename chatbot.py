# chatbot.py

from retrieval_chain import build_retrieval_chain

def main():
    print("\n🔍 Retrieval-Augmented Chatbot Initialized")
    print("Type your question or 'exit' to quit.")

    qa_chain = build_retrieval_chain()

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Exiting chat.")
            break

        try:
            result = qa_chain.invoke(user_input)
            print("\n🤖 Bot:", result['result'])

            if 'source_documents' in result:
                print("\n📚 Retrieved Context:")
                for i, doc in enumerate(result['source_documents']):
                    print(f"\n[{i+1}] {doc.page_content.strip()}")

        except Exception as e:
            print("⚠️ An error occurred:", str(e))

if __name__ == "__main__":
    main()
