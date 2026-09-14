"""Custom error classes for Threads operations."""

class ThreadsError(Exception):
    """Base exception for all Threads client errors."""
    pass

class AuthError(ThreadsError):
    """Raised when authentication credentials or session tokens are invalid or expired."""
    pass

class ChallengeRequiredError(ThreadsError):
    """Raised when Meta challenges the account (SMS/Email checkpoint)."""
    def __init__(self, message: str, challenge_url: str | None = None):
        super().__init__(message)
        self.challenge_url = challenge_url

class RateLimitError(ThreadsError):
    """Raised when Meta rate limits or throttles actions (HTTP 429)."""
    pass

class PostNotFoundError(ThreadsError):
    """Raised when target thread post does not exist or was deleted."""
    pass

class ServerError(ThreadsError):
    """Raised when Meta internal gateway fails (HTTP 5xx)."""
    pass
