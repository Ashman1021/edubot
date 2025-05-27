"""
EduBot - Academic AI Assistant
Main Streamlit application file.
"""

import streamlit as st
from config.settings import Config
from utils.helpers import initialize_session_state
from ui.sidebar import setup_sidebar
from ui.chat_interface import display_chat_history, display_welcome_message, handle_user_input

def setup_page_config() -> None:
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="EduBot - Your AI Academic Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def display_header() -> None:
    """Display the main header and status."""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.title("🤖 EduBot - Your AI Academic Assistant")
    
    with col2:
        # Status display
        if st.session_state.api_client:
            st.success("🟢 Connected")
            if st.button("🗑️ Clear Chat"):
                st.session_state.conversation_history = []
                st.session_state.total_tokens = 0
                st.rerun()
        else:
            st.error("🔴 No API Key Found")

def display_setup_instructions() -> None:
    """Display setup instructions when API key is not available."""
    st.error("⚠️ Please set your GEMINI_API_KEY environment variable!")
    st.markdown("""
    ### Setup Instructions:
    
    1. Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
    
    2. Set environment variable:
    ```bash
    # Linux/Mac
    export GEMINI_API_KEY="your-api-key-here"
    
    # Windows Command Prompt
    set GEMINI_API_KEY=your-api-key-here
    
    # Windows PowerShell
    $env:GEMINI_API_KEY="your-api-key-here"
    ```
    
    3. Restart the application
    
    ### Features:
    - 🖼️ **Image Analysis** for diagrams and handwritten notes
    - 📄 **Document Processing** for PDFs and spreadsheets  
    - 🌐 **Web Search Integration** for current information
    - 📚 **Academic assistance** across all subjects
    """)

def main() -> None:
    """Main application function."""
    
    setup_page_config()
    initialize_session_state()
    setup_sidebar()
    display_header()
    
    # Check if API client is available
    if not st.session_state.api_client:
        display_setup_instructions()
        return
    
    st.markdown("---")
    
    # Display chat interface
    if st.session_state.conversation_history:
        st.subheader("💬 Chat History")
        display_chat_history()
    else:
        display_welcome_message()
    
    # Handle user input
    if user_input := st.chat_input("Ask me anything academic! 🎓", key="chat_input"):
        handle_user_input(user_input)
        st.rerun()

if __name__ == "__main__":
    main()