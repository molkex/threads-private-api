"""Main Threads mobile protocol client."""
from __future__ import annotations
import httpx
from typing import Optional, Dict, Any, List
from .remote_signer import RemoteSigner
from .errors import ThreadsError, AuthError, RateLimitError, ServerError
from .modules.user import UserModule
from .modules.content import ContentModule
from .modules.feed import FeedModule
from .modules.search import SearchModule
from .modules.social import SocialModule
from .devices import get_threads_device, ThreadsDevicePreset
from .types import ThreadPost, DiscussionTree

class ThreadsAPI:
    """Headless Threads (com.instagram.barcelona) Mobile Protocol Client."""

    BASE_URL = "https://i.instagram.com"

    def __init__(
        self,
        api_key: str = "",
        *,
        session: Optional["ThreadsSession"] = None,
        session_token: Optional[str] = None,
        signing_server: str = "http://127.0.0.1:8643",
        device_preset: str = "threads_ios",
        proxy: Optional[str] = None,
        timeout: float = 15.0,
    ):
        self.api_key = api_key
        self.session = session
        if session is not None:
            if session.session_token and not session_token:
                session_token = session.session_token
            if session.device_preset:
                device_preset = session.device_preset

        self.session_token = session_token
        self.device_preset = device_preset
        self.device: ThreadsDevicePreset = get_threads_device(device_preset)
        self.signer = RemoteSigner(signing_server, api_key, device_preset=device_preset)

        client_kwargs = {"timeout": timeout}
        if proxy:
            client_kwargs["proxy"] = proxy

        self._http = httpx.Client(**client_kwargs)

        # Initialize submodules
        self.user = UserModule(self)
        self.content = ContentModule(self)
        self.feed = FeedModule(self)
        self.search = SearchModule(self)
        self.social = SocialModule(self)

    # High-level shortcuts
    def search_posts(self, query: str, limit: int = 15) -> List[ThreadPost]:
        """Sub-80ms real-time keyword search across public Threads discussions."""
        return self.search.search_posts(query=query, limit=limit)

    def reply(self, parent_post_id: str | int, text: str, reply_control: str = "everyone") -> dict:
        """Reply directly to any external thread post."""
        return self.content.reply(parent_post_id=parent_post_id, text=text, reply_control=reply_control)

    def like(self, post_id: str | int) -> dict:
        """Like a thread post."""
        return self.content.like(post_id=post_id)

    def repost(self, post_id: str | int) -> dict:
        """Repost / amplify a thread."""
        return self.content.repost(post_id=post_id)

    def get_thread(self, post_id: str | int) -> DiscussionTree:
        """Extract full nested discussion tree with replies."""
        return self.content.get_thread(post_id=post_id)

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> dict:
        signed = self.signer.sign_request(endpoint=path, method="GET")
        headers = signed.get("headers", {})
        if self.session_token:
            headers["Authorization"] = f"Bearer {self.session_token}"

        resp = self._http.get(f"{self.BASE_URL}{path}", params=params, headers=headers)
        return self._handle_response(resp)

    def _post(self, path: str, data: Optional[Dict[str, Any]] = None) -> dict:
        signed = self.signer.sign_request(endpoint=path, method="POST", body=data)
        headers = signed.get("headers", {})
        if self.session_token:
            headers["Authorization"] = f"Bearer {self.session_token}"

        payload = signed.get("signed_body", data or {})
        resp = self._http.post(f"{self.BASE_URL}{path}", data=payload, headers=headers)
        return self._handle_response(resp)

    def _handle_response(self, resp: httpx.Response) -> dict:
        if resp.status_code == 401:
            raise AuthError("Threads authentication failed or session expired.")
        if resp.status_code == 429:
            raise RateLimitError("Threads rate limit (429) encountered.")
        if resp.status_code >= 500:
            raise ServerError(f"Threads server error: {resp.status_code}")
        try:
            return resp.json()
        except Exception:
            return {"status": "ok", "status_code": resp.status_code, "text": resp.text[:200]}

    def close(self):
        self._http.close()
        self.signer.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
