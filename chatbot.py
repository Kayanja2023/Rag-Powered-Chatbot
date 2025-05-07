from retrieval_chain import build_retrieval_chain

def main():
    print("\nRetrieval-Augmented Chatbot Initialized")
    print("Type your question or 'exit' to quit.")

    qa_chain = build_retrieval_chain()
    session_id = "user"  # could be user ID or UUID for multi-user setup

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting chat.")
            break

        try:
            result = qa_chain.invoke(
                {"question": user_input},
                config={"configurable": {"session_id": session_id}}
            )

            # Handover trigger detection (uncertainty fallback)
            handover_triggers = [
                "i don't know",
                "i'm not sure",
                "unable to find",
                "not covered",
                "not in the provided documents",
                "i do not have enough information"
            ]

            response_lower = result.lower()

            if any(trigger in response_lower for trigger in handover_triggers):
                print("\n Bot: I'm not confident I can assist with that. Let me connect you to a live agent.")
            else:
                print("\n Bot:", result)

        except Exception as e:
            print(" An error occurred:", str(e))

if __name__ == "__main__":
    main()
