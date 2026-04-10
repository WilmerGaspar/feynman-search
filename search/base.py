from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class SearchResult:
    """Standard search result format"""

    title: str
    url: str
    snippet: str
    source: str
    date: Optional[datetime] = None
    authors: Optional[List[str]] = None
    doi: Optional[str] = None
    arxiv_id: Optional[str] = None

    def to_dict(self):
        return {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
            "source": self.source,
            "date": self.date.isoformat() if self.date else None,
            "authors": self.authors,
            "doi": self.doi,
            "arxiv_id": self.arxiv_id,
        }


class SearchBackend(ABC):
    """Base class for search backends"""

    @abstractmethod
    def search(self, query: str, max_results: int = 10, **kwargs) -> List[SearchResult]:
        """Execute search query"""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Return backend name"""
        pass
