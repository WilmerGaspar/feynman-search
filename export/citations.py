from typing import Optional, List
from search.base import SearchResult


class CitationFormatter:
    """Format citations in APA and IEEE styles"""

    @staticmethod
    def format_apa(result: SearchResult) -> str:
        """Format result as APA citation"""
        authors = result.authors or ["Unknown Author"]
        author_str = ", ".join(authors[:3])
        if len(authors) > 3:
            author_str += ", et al."

        year = result.date.year if result.date else "n.d."

        if result.arxiv_id or result.doi:
            if result.doi:
                doi_url = f"https://doi.org/{result.doi}"
                return (
                    f"{author_str} ({year}). {result.title}. Retrieved from {doi_url}"
                )
            else:
                arxiv_url = f"https://arxiv.org/abs/{result.arxiv_id}"
                return (
                    f"{author_str} ({year}). {result.title}. Retrieved from {arxiv_url}"
                )
        else:
            return f"{author_str} ({year}). {result.title}. Retrieved from {result.url}"

    @staticmethod
    def format_ieee(result: SearchResult) -> str:
        """Format result as IEEE citation"""
        authors = result.authors or ["Unknown Author"]
        if len(authors) == 1:
            author_str = authors[0]
        elif len(authors) == 2:
            author_str = f"{authors[0]} and {authors[1]}"
        else:
            author_str = f"{authors[0]}, et al."

        year = result.date.year if result.date else "n.d."
        source = result.source

        if result.doi:
            return (
                f'{author_str}, "{result.title}," {source}, {year}, doi: {result.doi}.'
            )
        else:
            return f'{author_str}, "{result.title}," {source}, {year}. [Online]. Available: {result.url}'

    @staticmethod
    def format_bibliography(results: List[SearchResult], style: str = "APA") -> str:
        """Generate formatted bibliography"""
        formatter = (
            CitationFormatter.format_apa
            if style == "APA"
            else CitationFormatter.format_ieee
        )

        citations = []
        for i, result in enumerate(results, 1):
            citation = formatter(result)
            citations.append(f"[{i}] {citation}")

        return "\n\n".join(citations)
