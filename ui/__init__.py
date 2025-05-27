"""UI package for EduBot."""

from .sidebar import setup_sidebar, process_uploaded_files, process_uploaded_images
from .chat_interface import display_chat_history, display_welcome_message, handle_user_input

__all__ = [
    'setup_sidebar', 
    'process_uploaded_files', 
    'process_uploaded_images',
    'display_chat_history', 
    'display_welcome_message', 
    'handle_user_input'
]