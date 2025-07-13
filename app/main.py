"""
Main Streamlit application for Clickatell AI Assistant
"""

import streamlit as st
import sys
import os
import hashlib

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Page configuration
st.set_page_config(
    page_title="Clickatell AI Assistant",
    page_icon="💬",
    layout="wide"
)

# CSS
st.markdown("""
<style>
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 1rem 0;
        max-width: 80%;
        margin-left: auto;
    }
    
    .bot-message {
        background: #f8f9fa;
        color: #2c3e50;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 1rem 0;
        max-width: 80%;
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'processed_hashes' not in st.session_state:
        st.session_state.processed_hashes = set()
    if 'pending_handover' not in st.session_state:
        st.session_state.pending_handover = False
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    if 'qa_chain' not in st.session_state:
        try:
            legacy_path = os.path.join(parent_dir, 'legacy')
            sys.path.insert(0, legacy_path)
            from retrieval_chain import build_retrieval_chain
            with st.spinner("Initializing AI Assistant..."):
                st.session_state.qa_chain = build_retrieval_chain()
        except Exception as e:
            st.error(f"Failed to initialize AI: {e}")
            st.session_state.qa_chain = None

def get_message_hash(message):
    return hashlib.md5(message.encode()).hexdigest()

def is_fallback_response(response):
    fallback_keywords = [
        "i'm not confident",
        "let me connect you to a live agent",
        "i'm unable to assist"
    ]
    return any(keyword in response.lower() for keyword in fallback_keywords)

def process_message(user_input):
    if not user_input.strip():
        return
    
    message_hash = get_message_hash(user_input)
    
    if message_hash in st.session_state.processed_hashes:
        return
    
    if st.session_state.processing:
        return
    
    st.session_state.processing = True
    st.session_state.processed_hashes.add(message_hash)
    
    try:
        if st.session_state.pending_handover:
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            if user_input.lower().strip() in ["yes", "y"]:
                response = "Connecting you to a live agent..."
                st.session_state.pending_handover = False
            elif user_input.lower().strip() in ["no", "n"]:
                response = "No problem! Feel free to ask another question."
                st.session_state.pending_handover = False
            else:
                response = "Please respond with 'yes' or 'no'."
            
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            if st.session_state.qa_chain:
                response = st.session_state.qa_chain.invoke(
                    {"input": user_input},
                    config={"configurable": {"session_id": "user-session"}}
                )
                
                if is_fallback_response(response):
                    response = "I'm not confident I can assist with that. Would you like me to connect you to a live agent? (yes/no)"
                    st.session_state.pending_handover = True
            else:
                response = "AI system not available. Please check configuration."
            
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    except Exception as e:
        st.session_state.messages.append({"role": "assistant", "content": f"Error: {str(e)}"})
    
    finally:
        st.session_state.processing = False

def main():
    initialize_session_state()
    
    st.title("💬 Clickatell AI Assistant")
    st.markdown("Your intelligent companion for Chat Commerce solutions")
    
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                <strong>You:</strong> {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="bot-message">
                <strong>🤖 Assistant:</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
    
    with st.form("chat_form", clear_on_submit=True):
        if st.session_state.pending_handover:
            st.info("Please respond with 'yes' or 'no' to connect to a live agent.")
        
        user_input = st.text_input(
            "Type your message:",
            placeholder="e.g., What is Clickatell's mission?",
            disabled=st.session_state.processing
        )
        
        submitted = st.form_submit_button(
            "Send", 
            disabled=st.session_state.processing or not user_input.strip()
        )
        
        if submitted and user_input.strip():
            process_message(user_input.strip())
            st.rerun()
    
    with st.sidebar:
        st.header("Quick Actions")
        
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.session_state.processed_hashes = set()
            st.session_state.pending_handover = False
            st.session_state.processing = False
            st.rerun()
        
        st.metric("Messages", len(st.session_state.messages))

if __name__ == "__main__":
    main()