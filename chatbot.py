# chatbot.py

from retrieval_chain import build_retrieval_chain


def main():
    print("\nRetrieval-Augmented Chatbot Initialized")
    print("Type your question or 'exit' to quit.")

    qa_chain = build_retrieval_chain()

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting chat.")
            break

        try:
            # Call the chain with the user query
            result = qa_chain.invoke({"query": user_input})

            # Check for uncertainty phrases in the output
            handover_triggers = [
                "i'm not sure",
                "i don't know",
                "i cannot answer",
                "no relevant information",
                "not enough information"
            ]

            if any(trigger in result['result'].lower() for trigger in handover_triggers):
                print("\n Bot: I'm not confident I can assist with that. Let me connect you to a live agent.")
            else:
                print("\n Bot:", result['result'])

        except Exception as e:
            print(" An error occurred:", str(e))


if __name__ == "__main__":
    main()
