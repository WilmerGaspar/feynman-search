import arxiv
from search.base import SearchBackend, SearchResult
from typing import List
from datetime import datetime
import streamlit as st


class ArxivBackend(SearchBackend):
    """arXiv scientific papers search backend"""

    def get_name(self) -> str:
        return "arXiv Papers"

    def search(self, query: str, max_results: int = 10, **kwargs) -> List[SearchResult]:
        """Search arXiv for scientific papers"""
        try:
            client = arxiv.Client()
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance,
                sort_order=arxiv.SortOrder.Descending,
            )

            search_results = []
            for entry in client.results(search):
                authors = [author.name for author in entry.authors]

                search_result = SearchResult(
                    title=entry.title,
                    url=entry.entry_id,
                    snippet=entry.summary[:500],
                    source="arXiv",
                    date=entry.published,
                    authors=authors,
                    arxiv_id=entry.entry_id.split("/abs/")[-1],
                )
                search_results.append(search_result)

            return search_results

        except Exception as e:
            st.error(f"arXiv search error: {str(e)}")
            return []
