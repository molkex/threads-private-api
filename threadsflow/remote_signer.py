"""Signing client for Threads mobile protocol requests."""
from __future__ import annotations
import httpx
from typing import Dict, Any, Optional
from .errors import AuthError, ServerError
from .devices import get_threads_device

class RemoteSigner:
    """Dispatches cryptographic signing requests to the local or cloud signing daemon."""

    def __init__(
        self,
        signing_server: str = "http://127.0.0.1:8643",
        api_key: str = "",
        device_preset: str = "threads_ios",
        timeout: float = 10.0,
    ):
        self.signing_server = signing_server.rstrip("/")
        self.api_key = api_key
        self.device_preset = device_preset
        self.device = get_threads_device(device_preset)
        self._http = httpx.Client(timeout=timeout)

    def sign_request(
        self,
        endpoint: str,
        method: str = "POST",
        body: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Sign request through daemon or fallback to authentic local headers."""
        payload = {
            "api_key": self.api_key,
            "device_preset": self.device_preset,
            "endpoint": endpoint,
            "method": method.upper(),
            "platform": "threads",
            "body": body or {},
        }
        try:
            resp = self._http.post(f"{self.signing_server}/v1/sign", json=payload)
            if resp.status_code in (401, 403):
                raise AuthError("Threads signing authorization failed. Valid API key required.")
            if resp.status_code >= 500:
                raise ServerError(f"Signing daemon error: {resp.status_code}")
            return resp.json()
        except (AuthError, ServerError):
            raise
        except Exception:
            # Standalone fallback mode
            return self._fallback_local_sign(endpoint, method, body)

    def _fallback_local_sign(
        self,
        endpoint: str,
        method: str,
        body: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        headers = {
            "User-Agent": self.device.user_agent,
            "X-IG-App-ID": self.device.app_id,
            "X-Bloks-Version-Id": self.device.bloks_version_id,
            "X-IG-Capabilities": self.device.capabilities,
            "X-IG-Connection-Type": "WIFI",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        return {"headers": headers, "signed_body": body or {}}

    def close(self):
        self._http.close()
