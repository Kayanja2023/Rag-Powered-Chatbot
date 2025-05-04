# chatbot.py

from retrieval_chain import build_retrieval_chain

def main():
    # Introductory message to user
    print("\nRetrieval-Augmented Chatbot Initialized")
    print("Type your question or 'exit' to quit.")

    # Initialize the QA chain (RetrievalQA chain with FAISS + LLM)
    qa_chain = build_retrieval_chain()


    # Start interactive chat loop
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting chat.")
            break

        try:
            # Pass user query to the retrieval QA chain
            result = qa_chain.invoke(user_input)

            # Display the chatbot's answer
            print("\n Bot:", result['result'])


            # If context documents were retrieved, print them
            if 'source_documents' in result:
                print("\nRetrieved Context:")
                for i, doc in enumerate(result['source_documents']):
                    print(f"\n[{i+1}] {doc.page_content.strip()}")
        # Catch and print any runtime errors
        except Exception as e:
            print(" An error occurred:", str(e))

if __name__ == "__main__":
    main()
