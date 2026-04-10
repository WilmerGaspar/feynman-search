import requests
from search.base import SearchBackend, SearchResult
from typing import List
from datetime import datetime
import streamlit as st


class SemanticScholarBackend(SearchBackend):
    """Semantic Scholar API backend for academic papers"""

    BASE_URL = "https://api.semanticscholar.org/graph/v1"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Feynman-Search/1.0"})

    def get_name(self) -> str:
        return "Semantic Scholar"

    def search(self, query: str, max_results: int = 10, **kwargs) -> List[SearchResult]:
        """Search Semantic Scholar for academic papers"""
        try:
            url = f"{self.BASE_URL}/paper/search"
            params = {
                "query": query,
                "limit": max_results,
                "fields": "title,authors,year,venue,url,publicationDate,abstract",
            }

            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            search_results = []
            for paper in data.get("data", []):
                authors = [author["name"] for author in paper.get("authors", [])]

                pub_date = None
                if paper.get("publicationDate"):
                    try:
                        pub_date = datetime.fromisoformat(paper["publicationDate"])
                    except:
                        pass

                search_result = SearchResult(
                    title=paper.get("title", "Untitled"),
                    url=paper.get("url", ""),
                    snippet=paper.get("abstract", "")[:500],
                    source="Semantic Scholar",
                    date=pub_date,
                    authors=authors,
                    doi=paper.get("doi"),
                )
                search_results.append(search_result)

            return search_results

        except Exception as e:
            st.error(f"Semantic Scholar search error: {str(e)}")
            return []
