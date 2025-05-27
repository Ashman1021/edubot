"""Chat interface components for EduBot."""

import streamlit as st
from utils.helpers import is_academic_question, prepare_context

def display_chat_history() -> None:
    """Display the chat conversation."""
    for message in st.session_state.conversation_history:
        if message["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.write(message["content"])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.write(message["content"])

def display_welcome_message() -> None:
    """Display welcome message when no conversation history exists."""
    st.markdown("""
    ### 👋 Hello! I'm EduBot, your AI academic assistant!
    
    I'm here to help you with:
    - 📚 **Academic subjects** (Math, Science, Literature, History, etc.)
    - 🖼️ **Image analysis** (diagrams, charts, handwritten notes)
    - 📄 **Document analysis** (PDFs, Word docs, spreadsheets)
    - 🧮 **Problem solving** and step-by-step explanations
    - 📝 **Homework help** and academic projects
    
    **What would you like to learn about today?**
    """)

def handle_user_input(user_input: str) -> None:
    """Handle user input and generate response."""
    
    if not is_academic_question(user_input):
        st.warning("⚠️ EduBot is designed for academic and educational questions only.")
        return
    
    st.session_state.conversation_history.append({"role": "user", "content": user_input})
    
    # Prepare context with documents and web search
    enhanced_input = prepare_context(
        st.session_state.uploaded_documents,
        user_input,
        st.session_state.web_search_enabled
    )
    
    # Prepare messages for API
    messages = _prepare_messages_for_api(enhanced_input)
    
    # Handle image context
    image_data = None
    if st.session_state.uploaded_images:
        image_data = st.session_state.uploaded_images[0]['base64_data']
    
    # Generate response
    _generate_and_display_response(messages, image_data)

def _prepare_messages_for_api(enhanced_input: str) -> list:
    """Prepare messages for API call."""
    messages = []
    
    # Include recent conversation history (last 10 messages)
    recent_history = st.session_state.conversation_history[-11:-1]
    for msg in recent_history:
        messages.append(msg)
    
    messages.append({"role": "user", "content": enhanced_input})
    return messages

def _generate_and_display_response(messages: list, image_data: str = None) -> None:
    """Generate and display AI response."""
    with st.spinner("🤔 EduBot is thinking..."):
        response = st.session_state.api_client.generate_response(
            messages=messages,
            image_data=image_data
        )
    
    if response["success"]:
        st.session_state.conversation_history.append({
            "role": "assistant", 
            "content": response["answer"]
        })
        
        if "usage" in response:
            st.session_state.total_tokens += response["usage"].get("totalTokenCount", 0)
        
    else:
        st.error(f"❌ Error: {response.get('error', 'Unknown error occurred')}")