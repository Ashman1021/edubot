"""Processors package for EduBot."""

from .document_processor import DocumentProcessor
from .image_processor import ImageProcessor
from .web_searcher import WebSearcher

__all__ = ['DocumentProcessor', 'ImageProcessor', 'WebSearcher']