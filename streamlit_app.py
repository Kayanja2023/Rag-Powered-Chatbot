import streamlit as st
from legacy.retrieval_chain import build_retrieval_chain
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Clickatell AI Assistant",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
    }
    
    /* Message styling */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 1rem 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3);
    }
    
    .bot-message {
        background: #f8f9fa;
        color: #2c3e50;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 1rem 0;
        max-width: 80%;
        border-left: 4px solid #667eea;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #e1e5e9;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'qa_chain' not in st.session_state:
        with st.spinner("🚀 Initializing Clickatell AI Assistant..."):
            st.session_state.qa_chain = build_retrieval_chain()
    if 'session_id' not in st.session_state:
        st.session_state.session_id = "user-session"
    if 'total_queries' not in st.session_state:
        st.session_state.total_queries = 0
    if 'processing' not in st.session_state:
        st.session_state.processing = False

def display_header():
    """Display the modern header"""
    st.markdown("""
    <div class="header-container">
        <div class="header-title">💬 Clickatell AI Assistant</div>
        <div class="header-subtitle">Your intelligent companion for Chat Commerce solutions</div>
    </div>
    """, unsafe_allow_html=True)

def process_user_input(user_input):
    """Process user input and generate response"""
    if st.session_state.processing:
        return
    
    st.session_state.processing = True
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.total_queries += 1
    
    try:
        response = st.session_state.qa_chain.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": st.session_state.session_id}}
        )
        
        if "I'm not confident I can assist with that" in response:
            response = "🤝 I'm not confident I can assist with that. Let me connect you to a live agent for better support."
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        
    except Exception as e:
        error_message = f"⚠️ Sorry, I encountered an error: {str(e)}"
        st.session_state.messages.append({"role": "assistant", "content": error_message})
    
    finally:
        st.session_state.processing = False

def display_sidebar():
    """Display the modern sidebar"""
    with st.sidebar:
        st.markdown("### 🎯 Quick Actions")
        
        quick_queries = [
            "What is Clickatell's mission?",
            "How do I authenticate API requests?",
            "What services are in Chat Commerce Platform?",
            "Who is the CEO of Clickatell?",
            "What does the Interact plan include?"
        ]
        
        st.markdown("**💡 Try these questions:**")
        for i, query in enumerate(quick_queries):
            if st.button(query, key=f"quick_{i}"):
                process_user_input(query)
                st.rerun()
        
        st.divider()
        
        st.markdown("### 📊 Session Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Queries", st.session_state.total_queries)
        with col2:
            st.metric("Messages", len(st.session_state.messages))
        
        if st.button("🗑️ Clear Chat", type="secondary"):
            st.session_state.messages = []
            st.session_state.total_queries = 0
            st.rerun()

def main():
    """Main application function"""
    initialize_session_state()
    display_header()
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Display chat messages
        chat_container = st.container()
        with chat_container:
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
                        <strong>🤖 Clickatell Assistant:</strong><br>
                        {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Show processing indicator
        if st.session_state.processing:
            with st.spinner("🤔 Thinking..."):
                st.empty()
        
        st.markdown("### 💭 Ask me anything about Clickatell")
        
        # Chat input form with Enter key support
        with st.form(key="chat_form", clear_on_submit=True):
            user_input = st.text_input(
                "Type your message here...",
                placeholder="e.g., How do I send a test SMS?",
                key="user_input",
                disabled=st.session_state.processing
            )
            
            submitted = st.form_submit_button(
                "📤 Send" if not st.session_state.processing else "Processing...",
                type="primary",
                disabled=st.session_state.processing
            )
            
            if submitted and user_input.strip() and not st.session_state.processing:
                process_user_input(user_input.strip())
                st.rerun()
    
    with col2:
        display_sidebar()
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem; padding: 1rem;">
        <p>🚀 Powered by Clickatell AI • Built with Streamlit</p>
        <p>💡 Ask me about Chat Commerce, APIs, pricing, and more!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()