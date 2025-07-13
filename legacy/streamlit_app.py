import streamlit as st
import time
from retrieval_chain import build_retrieval_chain
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
    
    /* Chat container styling */
    .chat-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        border: 1px solid #e1e5e9;
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
    
    /* Sidebar styling */
    .sidebar-content {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    /* Metrics styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 3px 15px rgba(0,0,0,0.08);
        text-align: center;
        margin: 0.5rem 0;
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
    if 'clear_input' not in st.session_state:
        st.session_state.clear_input = False
    if 'pending_handover' not in st.session_state:
        st.session_state.pending_handover = False

def display_header():
    """Display the modern header"""
    st.markdown("""
    <div class="header-container">
        <div class="header-title">💬 Clickatell AI Assistant</div>
        <div class="header-subtitle">Your intelligent companion for Chat Commerce solutions</div>
    </div>
    """, unsafe_allow_html=True)

def display_sidebar():
    """Display the modern sidebar"""
    with st.sidebar:
        st.markdown("### 🎯 Quick Actions")
        
        # Quick query buttons
        quick_queries = [
            "What is Clickatell's mission?",
            "How do I authenticate API requests?",
            "What services are in Chat Commerce Platform?",
            "Who is the CEO of Clickatell?",
            "What does the Interact plan include?"
        ]
        
        st.markdown("**💡 Try these questions:**")
        for query in quick_queries:
            if st.button(query, key=f"quick_{query[:20]}", help="Click to ask this question"):
                st.session_state.current_query = query
                st.rerun()
        
        st.divider()
        
        # Session metrics
        st.markdown("### 📊 Session Stats")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Queries", st.session_state.total_queries, delta=1 if st.session_state.total_queries > 0 else None)
        with col2:
            st.metric("Messages", len(st.session_state.messages))
        
        # Session info
        st.markdown("### ℹ️ Session Info")
        st.info(f"**Session ID:** {st.session_state.session_id}")
        st.info(f"**Started:** {datetime.now().strftime('%H:%M')}")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", type="secondary"):
            st.session_state.messages = []
            st.session_state.total_queries = 0
            st.session_state.pending_handover = False
            st.rerun()

def display_chat_interface():
    """Display the main chat interface"""
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages
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
    
    # Input area
    if hasattr(st.session_state, 'pending_handover') and st.session_state.pending_handover:
        st.markdown("### 🤝 Live Agent Handover")
        st.info("Please respond with 'yes' or 'no' to connect to a live agent.")
    else:
        st.markdown("### 💭 Ask me anything about Clickatell")
    
    # Handle quick query from sidebar
    default_query = ""
    if hasattr(st.session_state, 'current_query'):
        default_query = st.session_state.current_query
        delattr(st.session_state, 'current_query')
    
    # Clear input if flag is set
    if hasattr(st.session_state, 'clear_input') and st.session_state.clear_input:
        default_query = ""
        st.session_state.clear_input = False
    
    # Chat input
    user_input = st.text_input(
        "Type your message here...",
        value=default_query,
        placeholder="e.g., How do I send a test SMS?",
        key="chat_input"
    )
    
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        send_button = st.button("📤 Send", type="primary")
    
    with col2:
        if st.button("🎲 Random Question"):
            import random
            random_queries = [
                "What are Clickatell's main products?",
                "How does Chat2Pay work?",
                "What is the One API?",
                "Which countries does Clickatell operate in?",
                "What is Chat Flow used for?"
            ]
            st.session_state.current_query = random.choice(random_queries)
            st.rerun()
    
    # Process user input only when send button is clicked
    if send_button and user_input.strip():
        process_user_input(user_input.strip())
        # Clear the input by setting a flag
        st.session_state.clear_input = True
        st.rerun()

def process_user_input(user_input):
    """Process user input and generate response"""
    # Check if this message was already processed
    if (st.session_state.messages and 
        st.session_state.messages[-1]["role"] == "user" and 
        st.session_state.messages[-1]["content"] == user_input):
        return  # Already processed
    
    # Handle live agent handover state
    if hasattr(st.session_state, 'pending_handover') and st.session_state.pending_handover:
        if user_input.lower() in ["yes", "y"]:
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.messages.append({"role": "assistant", "content": "🔄 Connecting you to a live agent... Please wait while we transfer your conversation."})
            st.session_state.pending_handover = False
            return
        elif user_input.lower() in ["no", "n"]:
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.messages.append({"role": "assistant", "content": "👍 No problem! Feel free to ask me another question."})
            st.session_state.pending_handover = False
            return
        else:
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.messages.append({"role": "assistant", "content": "Please respond with 'yes' or 'no' to connect to a live agent."})
            return
    
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.total_queries += 1
    
    # Show typing indicator
    with st.spinner("🤔 Thinking..."):
        try:
            # Get response from the RAG chain
            response = st.session_state.qa_chain.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": st.session_state.session_id}}
            )
            
            # Check for fallback triggers
            fallback_keywords = [
                "i'm not confident",
                "let me connect you to a live agent",
                "i'm unable to assist",
                "i do not have that information"
            ]
            
            if any(keyword in response.lower() for keyword in fallback_keywords):
                response = "🤝 I'm not confident I can assist with that. Would you like me to connect you to a live agent? (Please respond with 'yes' or 'no')"
                st.session_state.pending_handover = True
            
            # Add bot response to chat
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            error_message = f"⚠️ Sorry, I encountered an error: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": error_message})

def display_analytics():
    """Display analytics dashboard"""
    if len(st.session_state.messages) > 0:
        st.markdown("### 📈 Conversation Analytics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Message count over time
            user_messages = [msg for msg in st.session_state.messages if msg["role"] == "user"]
            bot_messages = [msg for msg in st.session_state.messages if msg["role"] == "assistant"]
            
            fig = go.Figure(data=[
                go.Bar(name='Your Messages', x=['Messages'], y=[len(user_messages)], marker_color='#667eea'),
                go.Bar(name='Bot Responses', x=['Messages'], y=[len(bot_messages)], marker_color='#764ba2')
            ])
            fig.update_layout(
                title="Message Distribution",
                height=300,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Response time simulation (placeholder)
            response_times = [0.8, 1.2, 0.9, 1.1, 0.7][:len(bot_messages)]
            if response_times:
                fig = px.line(
                    x=list(range(1, len(response_times) + 1)),
                    y=response_times,
                    title="Response Times",
                    labels={'x': 'Query #', 'y': 'Seconds'}
                )
                fig.update_traces(line_color='#667eea', line_width=3)
                fig.update_layout(height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
        
        with col3:
            # Query categories (simulated)
            categories = ['Product Info', 'API Help', 'Pricing', 'Technical', 'General']
            values = [30, 25, 20, 15, 10]
            
            fig = px.pie(
                values=values,
                names=categories,
                title="Query Categories",
                color_discrete_sequence=px.colors.sequential.Plasma
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Display header
    display_header()
    
    # Create main layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Main chat interface
        display_chat_interface()
        
        # Analytics section
        if st.session_state.messages:
            with st.expander("📊 View Analytics", expanded=False):
                display_analytics()
    
    with col2:
        # Sidebar content
        display_sidebar()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem; padding: 1rem;">
        <p>🚀 Powered by Clickatell AI • Built with Streamlit</p>
        <p>💡 Ask me about Chat Commerce, APIs, pricing, and more!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()