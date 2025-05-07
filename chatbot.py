from retrieval_chain import build_retrieval_chain

def main():
    print("\nRetrieval-Augmented Chatbot Initialized")
    print("Type your question or 'exit' to quit.")

    qa_chain = build_retrieval_chain()
    session_id = "user-session"  # In production: generate or map user-specific ID

    fallback_keywords = [
        "i'm not confident",
        "let me connect you to a live agent"
    ]

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting chat.")
            break

        try:
            response = qa_chain.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": session_id}}
            )

            response_lower = response.lower()
            if any(trigger in response_lower for trigger in fallback_keywords):
                print("\nBot: I'm not confident I can assist with that. Let me connect you to a live agent.")
            else:
                print("\nBot:", response)

        except Exception as e:
            print("An error occurred:", str(e))

if __name__ == "__main__":
    main()
