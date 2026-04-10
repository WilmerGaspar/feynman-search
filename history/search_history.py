import json
import os
from datetime import datetime
from typing import List, Dict, Any
import streamlit as st
from config import HISTORY_FILE, MAX_HISTORY_ENTRIES
from search.base import SearchResult


class SearchHistory:
    """Manage search history in JSON file"""

    def __init__(self):
        self.history_file = HISTORY_FILE
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        """Create data directory if it doesn't exist"""
        os.makedirs(os.path.dirname(self.history_file) or ".", exist_ok=True)

    def _load(self) -> List[Dict[str, Any]]:
        """Load history from JSON file"""
        if not os.path.exists(self.history_file):
            return []

        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.warning(f"Error loading history: {str(e)}")
            return []

    def _save(self, history: List[Dict[str, Any]]):
        """Save history to JSON file"""
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            st.error(f"Error saving history: {str(e)}")

    def add_search(self, query: str, engine: str, results: List[SearchResult]):
        """Add search to history"""
        history = self._load()

        entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "engine": engine,
            "results_count": len(results),
            "results": [r.to_dict() for r in results],
        }

        history.insert(0, entry)
        history = history[:MAX_HISTORY_ENTRIES]

        self._save(history)

    def get_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent searches"""
        history = self._load()
        return history[:limit]

    def clear_history(self):
        """Clear all history"""
        self._save([])

    def get_stats(self) -> Dict[str, Any]:
        """Get history statistics"""
        history = self._load()

        if not history:
            return {"total": 0, "engines": {}, "recent_queries": []}

        engines = {}
        for entry in history:
            engine = entry["engine"]
            engines[engine] = engines.get(engine, 0) + 1

        recent_queries = [
            {
                "query": entry["query"],
                "timestamp": entry["timestamp"],
                "engine": entry["engine"],
                "results": entry["results_count"],
            }
            for entry in history[:10]
        ]

        return {
            "total": len(history),
            "engines": engines,
            "recent_queries": recent_queries,
        }
