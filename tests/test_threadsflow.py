"""Unit tests for threadsflow SDK."""
import json
import pytest
from unittest.mock import MagicMock, patch
from threadsflow import (
    ThreadsAPI,
    ThreadsSession,
    ThreadPost,
    ThreadAuthor,
    DiscussionTree,
    get_threads_device,
    ThreadsError,
    AuthError,
    RateLimitError,
)
from threadsflow.devices import THREADS_DEVICES
from threadsflow.mcp_server import handle_call_tool, TOOLS

def test_devices_presets():
    ios_dev = get_threads_device("threads_ios")
    assert ios_dev.platform == "iOS"
    assert "1546306509211461" == ios_dev.app_id
    assert "Barcelona" in ios_dev.user_agent

    android_dev = get_threads_device("threads_android")
    assert android_dev.platform == "Android"
    assert "3419628305025917" == android_dev.app_id
    assert "samsung" in android_dev.user_agent

    web_dev = get_threads_device("threads_web")
    assert web_dev.platform == "Web"

def test_session_serialization(tmp_path):
    sess = ThreadsSession(session_token="test_token_123", device_preset="threads_android")
    sess.user_id = "987654321"
    sess.cookies = {"sessionid": "sess_abc"}

    d = sess.to_dict()
    assert d["session_token"] == "test_token_123"
    assert d["device_preset"] == "threads_android"
    assert d["user_id"] == "987654321"

    filepath = str(tmp_path / "session.json")
    sess.save_to_file(filepath)

    loaded = ThreadsSession.load_from_file(filepath)
    assert loaded.session_token == "test_token_123"
    assert loaded.device_preset == "threads_android"
    assert loaded.user_id == "987654321"
    assert loaded.cookies == {"sessionid": "sess_abc"}

def test_threads_api_init_with_session():
    sess = ThreadsSession(session_token="tok_xyz", device_preset="threads_android")
    api = ThreadsAPI(session=sess)
    assert api.session_token == "tok_xyz"
    assert api.device_preset == "threads_android"
    assert api.device.platform == "Android"
    api.close()

def test_remote_signer_fallback():
    api = ThreadsAPI(device_preset="threads_ios")
    signed = api.signer._fallback_local_sign(
        endpoint="/api/v1/feed/text_post_app_timeline/",
        method="GET",
    )
    headers = signed["headers"]
    assert headers["X-IG-App-ID"] == "1546306509211461"
    assert "Barcelona" in headers["User-Agent"]
    api.close()

def test_search_posts_parsing():
    api = ThreadsAPI()
    mock_resp = {
        "list": [
            {
                "thread": {
                    "id": "3141592653589793238",
                    "pk": 3141592653589793238,
                    "code": "CxYz123",
                    "caption": {"text": "Excited to launch high throughput protocol engine!"},
                    "user": {
                        "pk": 12345678,
                        "username": "techlead",
                        "full_name": "Tech Lead",
                        "is_verified": True,
                    },
                    "like_count": 420,
                    "reply_count": 69,
                    "repost_count": 13,
                    "taken_at": 1726000000,
                }
            }
        ]
    }
    with patch.object(api, "_get", return_value=mock_resp):
        posts = api.search_posts(query="protocol", limit=5)
        assert len(posts) == 1
        post = posts[0]
        assert isinstance(post, ThreadPost)
        assert post.id == "3141592653589793238"
        assert post.caption == "Excited to launch high throughput protocol engine!"
        assert post.author.username == "techlead"
        assert post.author.is_verified is True
        assert post.like_count == 420
        assert post.reply_count == 69
    api.close()

def test_get_thread_tree_parsing():
    api = ThreadsAPI()
    mock_resp = {
        "containing_thread": {
            "thread_items": [
                {
                    "id": "1001",
                    "pk": 1001,
                    "code": "ROOT1",
                    "caption": {"text": "Root thread topic"},
                    "user": {"pk": 1, "username": "op_user"},
                }
            ]
        },
        "reply_threads": [
            {
                "thread_items": [
                    {
                        "id": "1002",
                        "pk": 1002,
                        "code": "REPLY1",
                        "caption": {"text": "First nested reply"},
                        "user": {"pk": 2, "username": "replier_1"},
                        "reply_to_post_id": "1001",
                    }
                ]
            }
        ]
    }
    with patch.object(api, "_get", return_value=mock_resp):
        tree = api.get_thread(post_id="1001")
        assert isinstance(tree, DiscussionTree)
        assert tree.root_post.id == "1001"
        assert tree.root_post.author.username == "op_user"
        assert len(tree.replies) == 1
        assert tree.replies[0].id == "1002"
        assert tree.replies[0].reply_to_post_id == "1001"
    api.close()

def test_reply_payload():
    api = ThreadsAPI()
    with patch.object(api, "_post", return_value={"status": "ok", "media": {"id": "2001"}}) as mock_post:
        res = api.reply(parent_post_id="1001", text="Agree 100%")
        assert res["status"] == "ok"
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert args[0] == "/api/v1/media/configure_text_post_app_feed/"
        data = kwargs["data"]
        assert data["caption"] == "Agree 100%"
        info = json.loads(data["text_post_app_info"])
        assert info["reply_to_post_id"] == "1001"
        assert info["reply_control"] == "everyone"
    api.close()

def test_social_module():
    api = ThreadsAPI()
    with patch.object(api, "_post", return_value={"friendship_status": {"following": True}}) as mock_post:
        res = api.social.follow("555123")
        assert res["friendship_status"]["following"] is True
        mock_post.assert_called_once_with("/api/v1/friendships/create/555123/")
    api.close()

def test_mcp_server_tools_list():
    assert len(TOOLS) >= 7
    names = [t["name"] for t in TOOLS]
    assert "threads_search_posts" in names
    assert "threads_reply_post" in names
    assert "threads_get_discussion_tree" in names
    assert "threads_publish_post" in names

def test_mcp_server_tool_search():
    mock_posts = [
        ThreadPost(
            id="1", pk=1, code="a", caption="test post",
            author=ThreadAuthor(pk=10, username="tester"),
            like_count=5, reply_count=2, repost_count=0, taken_at=1700000000,
        )
    ]
    with patch("threadsflow.mcp_server._get_client") as mock_client_getter:
        mock_client = MagicMock()
        mock_client.search_posts.return_value = mock_posts
        mock_client_getter.return_value = mock_client

        res = handle_call_tool("threads_search_posts", {"query": "test", "limit": 5})
        mock_client.search_posts.assert_called_once_with(query="test", limit=5)
        parsed = json.loads(res["content"][0]["text"])
        assert len(parsed) == 1
        assert parsed[0]["id"] == "1"
        assert parsed[0]["author"]["username"] == "tester"
