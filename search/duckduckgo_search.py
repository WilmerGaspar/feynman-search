from search.base import SearchBackend, SearchResult
from duckduckgo_search import DDGS
from typing import List
import streamlit as st


class DuckDuckGoBackend(SearchBackend):
    """DuckDuckGo web search backend"""

    def __init__(self):
        self.ddgs = DDGS(timeout=20)

    def get_name(self) -> str:
        return "DuckDuckGo Web"

    def search(self, query: str, max_results: int = 10, **kwargs) -> List[SearchResult]:
        """Search using DuckDuckGo"""
        try:
            results = self.ddgs.text(query, max_results=max_results)

            search_results = []
            for result in results:
                search_result = SearchResult(
                    title=result.get("title", "Untitled"),
                    url=result.get("href", ""),
                    snippet=result.get("body", ""),
                    source="DuckDuckGo",
                    date=None,
                )
                search_results.append(search_result)

            return search_results

        except Exception as e:
            st.error(f"DuckDuckGo search error: {str(e)}")
            return []
