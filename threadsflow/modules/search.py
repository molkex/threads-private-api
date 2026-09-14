"""Search, real-time keyword streams, and trend radar endpoints."""
from __future__ import annotations
from typing import Dict, Any, List
from ..types import ThreadPost

class SearchModule:
    """Sub-80ms search engine for public Threads posts and trending topics."""

    def __init__(self, client):
        self._client = client

    def search_posts(self, query: str, limit: int = 15) -> List[ThreadPost]:
        """
        Sub-80ms wire-speed keyword search across public Threads discussions.
        No browser rendering, no official App Review limitation.
        """
        params = {
            "query": query,
            "count": str(limit),
            "context": "bloks_search",
        }
        res = self._client._get("/api/v1/fbsearch/topsearch_flat/", params=params)
        posts = []
        for item in res.get("list", []):
            thread = item.get("thread") or item
            if thread:
                posts.append(ThreadPost.from_dict(thread))
        return posts

    def trending_topics(self) -> List[Dict[str, Any]]:
        """Fetch real-time trending topics, hashtags, and viral discussion prompts."""
        res = self._client._get("/api/v1/text_post_app/trending_topics/")
        return res.get("trending_topics", res.get("items", []))
