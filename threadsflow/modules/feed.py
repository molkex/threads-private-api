"""Feed, timeline, and notification discovery endpoints."""
from __future__ import annotations
from typing import Dict, Any, List

class FeedModule:
    """Operations on Threads timelines and notification feeds."""

    def __init__(self, client):
        self._client = client

    def timeline(self, max_id: str | None = None) -> dict:
        """Fetch recommended 'For You' Threads timeline feed."""
        params = {}
        if max_id:
            params["max_id"] = max_id
        return self._client._get("/api/v1/feed/text_post_app_timeline/", params=params or None)

    def following_timeline(self, max_id: str | None = None) -> dict:
        """Fetch chronological 'Following' timeline feed."""
        params = {}
        if max_id:
            params["max_id"] = max_id
        return self._client._get("/api/v1/feed/text_post_app_following_timeline/", params=params or None)

    def notifications(self, filter_type: str | None = None) -> dict:
        """Fetch activity notifications (replies, mentions, quotes, likes)."""
        params = {}
        if filter_type:
            params["filter_type"] = filter_type
        return self._client._get("/api/v1/text_post_app/news_feed/", params=params or None)

    def set_notifications_seen(self) -> dict:
        """Mark all incoming activity notifications as seen."""
        return self._client._post("/api/v1/text_post_app/news_feed_seen/")
