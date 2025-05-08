# Import the function that builds the retrieval-augmented chatbot pipeline
from retrieval_chain import build_retrieval_chain

def main():
    print("\nRetrieval-Augmented Chatbot Initialized")
    print("Type your question or 'exit' to quit.")

    qa_chain = build_retrieval_chain()
    session_id = "user-session"

    fallback_keywords = [
        "i'm not confident",
        "let me connect you to a live agent",
        "i'm unable to assist",
        "i do not have that information",
        "this may require a human agent",
        "cannot confidently answer",
        "not covered in the documents"
    ]

    pending_handover = False  # Track if we're awaiting user confirmation for live agent

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting chat.")
            break

        # Handle live agent confirmation
        if pending_handover:
            if user_input.lower() in ["yes", "y"]:
                print("Bot: Connecting you to a live agent...")
                break                                                       # Stop the chatbot to simulate handover
            elif user_input.lower() in ["no", "n"]:
                print("Bot: Okay, feel free to ask another question.")
                pending_handover = False
                continue                                                    # Skip rest of loop and prompt user again
            else:
                print("Bot: Please type 'yes' or 'no'.")
                continue


        # Invoke the retrieval-augmented chain with user input and session ID
        try:
            response = qa_chain.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": session_id}}
            )


            # Check if the response contains any fallback trigger phrases
            response_lower = response.lower()
            if any(trigger in response_lower for trigger in fallback_keywords):
                print("\nBot: I'm not confident I can assist with that. Would you like me to connect you to a live agent? (yes/no)")
                pending_handover = True
            else:
                print("\nBot:", response)

        except Exception as e:
            print("An error occurred:", str(e))

if __name__ == "__main__":
    main()
