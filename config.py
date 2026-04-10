import os
from datetime import datetime, timedelta

# Search engines
SEARCH_ENGINES = {
    "web": "DuckDuckGo Web",
    "arxiv": "arXiv Papers",
    "scholar": "Semantic Scholar",
}

# API settings
ARXIV_MAX_RESULTS = 50
SEMANTIC_SCHOLAR_MAX_RESULTS = 50
DUCKDUCKGO_MAX_RESULTS = 50

# History settings
HISTORY_FILE = "data/search_history.json"
MAX_HISTORY_ENTRIES = 500

# PDF settings
PDF_STYLES = {"title_size": 24, "heading_size": 14, "body_size": 11, "margin": 72}

# Citation formats
CITATION_FORMATS = ["APA", "IEEE"]

# Date filtering
DATE_FILTERS = {
    "any": None,
    "past_week": timedelta(days=7),
    "past_month": timedelta(days=30),
    "past_year": timedelta(days=365),
}
