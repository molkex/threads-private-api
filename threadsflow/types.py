"""Domain models and dataclasses for Threads entities."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class ThreadAuthor:
    pk: int
    username: str
    full_name: str = ""
    profile_pic_url: str = ""
    is_verified: bool = False

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ThreadAuthor:
        u = data.get("user", data)
        return cls(
            pk=int(u.get("pk", 0)),
            username=str(u.get("username", "")),
            full_name=str(u.get("full_name", "")),
            profile_pic_url=str(u.get("profile_pic_url", "")),
            is_verified=bool(u.get("is_verified", False)),
        )

@dataclass
class ThreadPost:
    id: str
    pk: int
    code: str
    caption: str
    author: ThreadAuthor
    like_count: int = 0
    reply_count: int = 0
    repost_count: int = 0
    taken_at: int = 0
    reply_to_post_id: Optional[str] = None
    media_type: int = 1  # 1 = text/photo, 2 = video

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ThreadPost:
        thread = data.get("thread", data)
        caption_dict = thread.get("caption") or {}
        caption_text = caption_dict.get("text", "") if isinstance(caption_dict, dict) else str(caption_dict)
        user_dict = thread.get("user") or {}
        return cls(
            id=str(thread.get("id", thread.get("pk", ""))),
            pk=int(thread.get("pk", thread.get("id", 0))),
            code=str(thread.get("code", "")),
            caption=caption_text,
            author=ThreadAuthor.from_dict(user_dict),
            like_count=int(thread.get("like_count", 0)),
            reply_count=int(thread.get("reply_count", 0)),
            repost_count=int(thread.get("repost_count", 0)),
            taken_at=int(thread.get("taken_at", 0)),
            reply_to_post_id=thread.get("reply_to_post_id"),
            media_type=int(thread.get("media_type", 1)),
        )

@dataclass
class DiscussionTree:
    root_post: ThreadPost
    replies: List[ThreadPost] = field(default_factory=list)
    has_more: bool = False
    cursor: Optional[str] = None
