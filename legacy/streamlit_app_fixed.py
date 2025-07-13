import streamlit as st
import time
import hashlib
from retrieval_chain import build_retrieval_chain
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Clickatell AI Assistant",
    page_icon="💬",
    layout="wide"
)

# Custom CSS
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

def get_message_hash(message):
    """Create unique hash for message to prevent duplicates"""
    return hashlib.md5(message.encode()).hexdigest()

def initialize_session_state():
    """Initialize session state with proper controls"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'processed_hashes' not in st.session_state:
        st.session_state.processed_hashes = set()
    if 'qa_chain' not in st.session_state:
        with st.spinner("Initializing AI Assistant..."):
            st.session_state.qa_chain = build_retrieval_chain()
    if 'session_id' not in st.session_state:
        st.session_state.session_id = "user-session"
    if 'pending_handover' not in st.session_state:
        st.session_state.pending_handover = False
    if 'processing' not in st.session_state:
        st.session_state.processing = False

def is_fallback_response(response):
    """Check if response indicates fallback needed"""
    fallback_keywords = [
        "i'm not confident",
        "let me connect you to a live agent",
        "i'm unable to assist",
        "i do not have that information",
        "cannot confidently answer"
    ]
    return any(keyword in response.lower() for keyword in fallback_keywords)

def process_message(user_input):
    """Process user message with strict duplicate prevention"""
    message_hash = get_message_hash(user_input)
    
    # Prevent duplicate processing
    if message_hash in st.session_state.processed_hashes:
        return
    
    # Prevent concurrent processing
    if st.session_state.processing:
        return
    
    st.session_state.processing = True
    st.session_state.processed_hashes.add(message_hash)
    
    try:
        # Handle live agent handover responses
        if st.session_state.pending_handover:
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            if user_input.lower().strip() in ["yes", "y"]:
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": "🔄 Connecting you to a live agent... Please wait."
                })
                st.session_state.pending_handover = False
            elif user_input.lower().strip() in ["no", "n"]:
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": "👍 No problem! Feel free to ask me another question."
                })
                st.session_state.pending_handover = False
            else:
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": "Please respond with 'yes' or 'no'."
                })
            
            st.session_state.processing = False
            return
        
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get AI response
        response = st.session_state.qa_chain.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": st.session_state.session_id}}
        )
        
        # Check for fallback
        if is_fallback_response(response):
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "🤝 I'm not confident I can assist with that. Would you like me to connect you to a live agent? (Please respond with 'yes' or 'no')"
            })
            st.session_state.pending_handover = True
        else:
            st.session_state.messages.append({"role": "assistant", "content": response})
        
    except Exception as e:
        st.session_state.messages.append({
            "role": "assistant", 
            "content": f"⚠️ Error: {str(e)}"
        })
    
    finally:
        st.session_state.processing = False

def main():
    initialize_session_state()
    
    st.title("💬 Clickatell AI Assistant")
    st.markdown("Your intelligent companion for Chat Commerce solutions")
    
    # Display messages
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
    
    # Input form to prevent auto-submission
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
    
    # Sidebar
    with st.sidebar:
        st.header("Quick Actions")
        
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.session_state.processed_hashes = set()
            st.session_state.pending_handover = False
            st.session_state.processing = False
            st.rerun()
        
        st.metric("Messages", len(st.session_state.messages))
        
        if st.session_state.pending_handover:
            st.warning("⏳ Waiting for live agent response")
        
        if st.session_state.processing:
            st.info("🔄 Processing...")

if __name__ == "__main__":
    main()