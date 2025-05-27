"""Web search functionality."""

from typing import List, Dict
from config.settings import Config

try:
    from duckduckgo_search import DDGS
    WEB_SEARCH_SUPPORT = True
except ImportError:
    WEB_SEARCH_SUPPORT = False

class WebSearcher:
    """Handle web search functionality."""
    
    @staticmethod
    def is_supported() -> bool:
        """Check if web search is supported."""
        return WEB_SEARCH_SUPPORT
    
    @staticmethod
    def search_web(query: str, max_results: int = None) -> List[Dict[str, str]]:
        """Search the web using DuckDuckGo."""
        max_results = max_results or Config.MAX_SEARCH_RESULTS
        
        try:
            if not WEB_SEARCH_SUPPORT:
                return [{"title": "Web Search Not Available", 
                        "body": "Please install duckduckgo-search: pip install duckduckgo-search",
                        "href": ""}]
            
            with DDGS() as ddgs:
                results = []
                for r in ddgs.text(query, max_results=max_results):
                    results.append({
                        "title": r.get("title", ""),
                        "body": r.get("body", ""),
                        "href": r.get("href", "")
                    })
                return results
        except Exception as e:
            return [{"title": "Search Error", 
                    "body": f"Error searching web: {str(e)}",
                    "href": ""}]
    
    @staticmethod
    def format_search_results(results: List[Dict[str, str]]) -> str:
        """Format search results for AI consumption."""
        formatted = "Web Search Results:\n\n"
        for i, result in enumerate(results, 1):
            formatted += f"{i}. **{result['title']}**\n"
            formatted += f"   {result['body']}\n"
            if result['href']:
                formatted += f"   Source: {result['href']}\n"
            formatted += "\n"
        return formatted