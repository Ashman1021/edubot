"""Helper functions for EduBot."""

import re
from typing import List, Dict, Any
from config.settings import Config

def is_academic_question(question: str) -> bool:
    """Check if the question is academic/educational in nature."""
    question_lower = question.lower()
    
    # Check for academic keywords
    for keyword in Config.ACADEMIC_KEYWORDS:
        if keyword in question_lower:
            return True
    
    # Check for mathematical expressions
    math_patterns = [
        r'\d+\s*[\+\-\*\/\=]\s*\d+',
        r'[xy]\s*[\+\-\*\/\=]',
        r'\b(sin|cos|tan|log|ln)\b'
    ]
    
    for pattern in math_patterns:
        if re.search(pattern, question_lower):
            return True
    
    # Check for code-related patterns
    code_patterns = [
        r'\b(print|return|if|else|for|while|function|def|class|import)\b',
        r'[\{\}\[\]\(\);]'
    ]
    
    for pattern in code_patterns:
        if re.search(pattern, question_lower):
            return True
    
    # Accept short questions as potentially academic
    if len(question.strip()) < 10:
        return True
    
    return False

def prepare_context(uploaded_documents: List[Dict], user_input: str, 
                   web_search_enabled: bool = True) -> str:
    """Prepare context from uploaded documents and web search."""
    context_parts = []
    
    # Add document context
    if uploaded_documents:
        context_parts.append("UPLOADED DOCUMENTS:")
        for doc in uploaded_documents:
            context_parts.append(f"\n--- {doc['name']} ({doc['type']}) ---")
            content = doc['content'][:Config.MAX_DOCUMENT_PREVIEW]
            context_parts.append(content)
        context_parts.append("\n" + "="*50 + "\n")
    
    # Handle web search
    if web_search_enabled and should_search_web(user_input):
        from processors.web_searcher import WebSearcher
        search_results = WebSearcher.search_web(user_input)
        search_context = WebSearcher.format_search_results(search_results)
        context_parts.append("WEB SEARCH RESULTS:")
        context_parts.append(search_context)
        context_parts.append("="*50 + "\n")
    
    if context_parts:
        return "\n".join(context_parts) + f"\nUSER QUESTION: {user_input}"
    else:
        return user_input

def should_search_web(user_input: str) -> bool:
    """Determine if web search should be performed."""
    search_keywords = ['current', 'latest', 'recent', 'today', 'news', '2024', '2025']
    return any(keyword in user_input.lower() for keyword in search_keywords)

def initialize_session_state() -> None:
    """Initialize Streamlit session state variables."""
    import streamlit as st
    from api.gemini_client import GeminiAPI
    from config.settings import Config
    
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    
    if "api_client" not in st.session_state:
        st.session_state.api_client = None
    
    if "total_tokens" not in st.session_state:
        st.session_state.total_tokens = 0
    
    if "uploaded_documents" not in st.session_state:
        st.session_state.uploaded_documents = []
    
    if "uploaded_images" not in st.session_state:
        st.session_state.uploaded_images = []
    
    if "web_search_enabled" not in st.session_state:
        st.session_state.web_search_enabled = True
    
    # Auto-connect if API key is available
    if Config.GEMINI_API_KEY and not st.session_state.api_client:
        try:
            st.session_state.api_client = GeminiAPI(Config.GEMINI_API_KEY)
        except Exception:
            pass