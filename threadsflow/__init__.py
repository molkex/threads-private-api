"""
threadsflow - Unofficial Threads Private API & Trend Radar SDK.
Headless protocol engine for Threads (com.instagram.barcelona).
"""

from .client import ThreadsAPI
from .session import ThreadsSession
from .types import ThreadAuthor, ThreadPost, DiscussionTree
from .devices import ThreadsDevicePreset, THREADS_DEVICES, get_threads_device
from .errors import (
    ThreadsError,
    AuthError,
    ChallengeRequiredError,
    RateLimitError,
    PostNotFoundError,
    ServerError,
)

# Friendly alias
ThreadsClient = ThreadsAPI

__version__ = "1.0.0"

__all__ = [
    "ThreadsAPI",
    "ThreadsClient",
    "ThreadsSession",
    "ThreadAuthor",
    "ThreadPost",
    "DiscussionTree",
    "ThreadsDevicePreset",
    "THREADS_DEVICES",
    "get_threads_device",
    "ThreadsError",
    "AuthError",
    "ChallengeRequiredError",
    "RateLimitError",
    "PostNotFoundError",
    "ServerError",
]
