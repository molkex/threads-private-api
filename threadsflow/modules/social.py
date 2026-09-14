"""Social graph moderation and relationship endpoints (shared Meta graph)."""
from __future__ import annotations

class SocialModule:
    """Operations on following, unfollowing, blocking, and muting (shared with Instagram)."""

    def __init__(self, client):
        self._client = client

    def follow(self, user_id: str | int) -> dict:
        """Follow user (reflects across both Threads and Instagram)."""
        return self._client._post(f"/api/v1/friendships/create/{user_id}/")

    def unfollow(self, user_id: str | int) -> dict:
        """Unfollow user."""
        return self._client._post(f"/api/v1/friendships/destroy/{user_id}/")

    def block(self, user_id: str | int) -> dict:
        """Block user."""
        return self._client._post(f"/api/v1/friendships/block/{user_id}/")

    def unblock(self, user_id: str | int) -> dict:
        """Unblock user."""
        return self._client._post(f"/api/v1/friendships/unblock/{user_id}/")

    def mute(self, user_id: str | int) -> dict:
        """Mute posts from user."""
        data = {"target_posts_author_id": str(user_id)}
        return self._client._post("/api/v1/friendships/mute_posts_or_story_from_follow/", data=data)

    def unmute(self, user_id: str | int) -> dict:
        """Unmute posts from user."""
        data = {"target_posts_author_id": str(user_id)}
        return self._client._post("/api/v1/friendships/unmute_posts_or_story_from_follow/", data=data)

    def restrict(self, user_id: str | int) -> dict:
        """Restrict user interaction."""
        return self._client._post(f"/api/v1/restrict_action/restrict_user/", data={"target_user_id": str(user_id)})

    def unrestrict(self, user_id: str | int) -> dict:
        """Unrestrict user."""
        return self._client._post(f"/api/v1/restrict_action/unrestrict_user/", data={"target_user_id": str(user_id)})
