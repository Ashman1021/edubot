"""Configuration settings for EduBot."""

import os
from typing import Optional

class Config:
    """Application configuration."""
    
    # API Configuration
    GEMINI_API_KEY: Optional[str] = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
    GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"
    
    # Model Configuration
    DEFAULT_MODEL = "gemini-1.5-flash"
    DEFAULT_MAX_TOKENS = 2000
    DEFAULT_TEMPERATURE = 0.7
    
    # File Processing
    MAX_IMAGE_SIZE = 1024
    MAX_DOCUMENT_PREVIEW = 2000
    
    # Search Configuration
    MAX_SEARCH_RESULTS = 3
    
    # Academic Keywords
    ACADEMIC_KEYWORDS = [
        'study', 'learn', 'education', 'school', 'university', 'college', 'academic',
        'research', 'theory', 'concept', 'principle', 'analysis', 'explain', 'definition',
        'homework', 'assignment', 'project', 'exam', 'test', 'quiz', 'lesson',
        'code', 'program', 'programming', 'algorithm', 'function', 'variable', 'loop',
        'math', 'mathematics', 'algebra', 'calculus', 'geometry', 'statistics',
        'science', 'physics', 'chemistry', 'biology', 'history', 'geography',
        'literature', 'english', 'writing', 'grammar', 'economics', 'psychology',
        'calculate', 'solve', 'derive', 'prove', 'analyze', 'compare', 'contrast',
        'what is', 'how does', 'why does', 'when did', 'where is', 'who was'
    ]
    
    # Safety Settings
    SAFETY_SETTINGS = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        }
    ]