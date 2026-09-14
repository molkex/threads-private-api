"""User profile, thread catalog, and author discovery endpoints."""
from __future__ import annotations
from typing import Dict, Any, List

class UserModule:
    """Operations on Threads user profiles, user thread tabs, and replies."""

    def __init__(self, client):
        self._client = client

    def info(self, user_id: str | int) -> dict:
        """Fetch comprehensive user profile information by numeric user ID."""
        return self._client._get(f"/api/v1/users/{user_id}/info/")

    def info_by_username(self, username: str) -> dict:
        """Fetch user profile metadata by username."""
        return self._client._get(f"/api/v1/users/{username}/usernameinfo/")

    def user_threads(self, user_id: str | int, max_id: str | None = None) -> dict:
        """Retrieve user's primary published threads tab."""
        params = {}
        if max_id:
            params["max_id"] = max_id
        return self._client._get(f"/api/v1/text_post_app/{user_id}/profile/threads/", params=params or None)

    def user_replies(self, user_id: str | int, max_id: str | None = None) -> dict:
        """Retrieve user's reply history tab."""
        params = {}
        if max_id:
            params["max_id"] = max_id
        return self._client._get(f"/api/v1/text_post_app/{user_id}/profile/replies/", params=params or None)

    def user_reposts(self, user_id: str | int, max_id: str | None = None) -> dict:
        """Retrieve user's reposted threads."""
        params = {}
        if max_id:
            params["max_id"] = max_id
        return self._client._get(f"/api/v1/text_post_app/{user_id}/profile/reposts/", params=params or None)

    def search_users(self, query: str, limit: int = 10) -> List[dict]:
        """Search accounts by keyword or bio match."""
        params = {
            "query": query,
            "count": str(limit),
            "context": "bloks_search_users",
        }
        res = self._client._get("/api/v1/fbsearch/topsearch_flat/", params=params)
        return res.get("list", [])
