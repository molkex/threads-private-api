"""Session state and token persistence for Threads client."""
from __future__ import annotations
import json
import os
from typing import Dict, Any, Optional

class ThreadsSession:
    """Manages serialization and disk persistence of authenticated Threads sessions."""

    def __init__(self, session_token: Optional[str] = None, device_preset: str = "threads_ios"):
        self.session_token = session_token
        self.device_preset = device_preset
        self.user_id: Optional[str] = None
        self.cookies: Dict[str, str] = {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_token": self.session_token,
            "device_preset": self.device_preset,
            "user_id": self.user_id,
            "cookies": self.cookies,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ThreadsSession:
        storage = cls(
            session_token=data.get("session_token"),
            device_preset=data.get("device_preset", "threads_ios")
        )
        storage.user_id = data.get("user_id")
        storage.cookies = data.get("cookies", {})
        return storage

    def save_to_file(self, filepath: str) -> None:
        dir_path = os.path.dirname(filepath)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load_from_file(cls, filepath: str) -> ThreadsSession:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)
