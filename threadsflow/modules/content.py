"""Thread publishing, direct replies to any post, quoting, liking, and tree ingestion."""
from __future__ import annotations
import json
import time
from typing import Dict, Any, List, Optional
from ..types import ThreadPost, DiscussionTree

class ContentModule:
    """Operations on Thread posts, replies, and discussion trees."""

    def __init__(self, client):
        self._client = client

    def publish_text(self, text: str, reply_control: str = "everyone") -> dict:
        """
        Publish a new top-level text thread.
        reply_control options: 'everyone', 'accounts_you_follow', 'mentioned_only'.
        """
        data = {
            "caption": text,
            "text_post_app_info": json.dumps({"reply_control": reply_control}),
        }
        return self._client._post("/api/v1/media/configure_text_post_app_feed/", data=data)

    def reply(self, parent_post_id: str | int, text: str, reply_control: str = "everyone") -> dict:
        """
        Reply directly to ANY public thread post without Meta App Review restrictions.
        """
        data = {
            "caption": text,
            "text_post_app_info": json.dumps({
                "reply_to_post_id": str(parent_post_id),
                "reply_control": reply_control,
            }),
        }
        return self._client._post("/api/v1/media/configure_text_post_app_feed/", data=data)

    def quote(self, quoted_post_id: str | int, text: str) -> dict:
        """Quote an existing thread post with added commentary."""
        data = {
            "caption": text,
            "text_post_app_info": json.dumps({
                "quoted_post_id": str(quoted_post_id),
            }),
        }
        return self._client._post("/api/v1/media/configure_text_post_app_feed/", data=data)

    def get_thread(self, post_id: str | int) -> DiscussionTree:
        """
        Retrieve complete nested discussion hierarchy (root post, parent, and recursive replies).
        """
        res = self._client._get(f"/api/v1/text_post_app/{post_id}/text_post_app_thread/")
        threads_data = res.get("containing_thread", res)
        root = ThreadPost.from_dict(threads_data.get("thread_items", [{}])[0])
        replies = []
        for item in res.get("reply_threads", []):
            for t_item in item.get("thread_items", []):
                replies.append(ThreadPost.from_dict(t_item))
        return DiscussionTree(root_post=root, replies=replies)

    def thread_likers(self, post_id: str | int) -> List[dict]:
        """Fetch list of accounts that liked this thread."""
        res = self._client._get(f"/api/v1/media/{post_id}/likers/")
        return res.get("users", [])

    def like(self, post_id: str | int) -> dict:
        """Like a thread post."""
        return self._client._post(f"/api/v1/media/{post_id}/like/")

    def unlike(self, post_id: str | int) -> dict:
        """Unlike a thread post."""
        return self._client._post(f"/api/v1/media/{post_id}/unlike/")

    def repost(self, post_id: str | int) -> dict:
        """Repost / amplify a thread to your followers."""
        return self._client._post(f"/api/v1/media/{post_id}/repost/")

    def unrepost(self, post_id: str | int) -> dict:
        """Remove a previously reposted thread."""
        return self._client._post(f"/api/v1/media/{post_id}/unrepost/")

    def delete(self, post_id: str | int) -> dict:
        """Delete an owned thread post."""
        data = {"media_id": str(post_id)}
        return self._client._post(f"/api/v1/media/{post_id}/delete/", data=data)
