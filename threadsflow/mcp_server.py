"""Model Context Protocol (MCP) Server for Threads (Barcelona) automation.

Run as an MCP server for Claude Desktop, Cursor, or Windsurf:
    python -m threadsflow.mcp_server
"""
from __future__ import annotations

import sys
import json
import os
from dataclasses import asdict
from .client import ThreadsAPI
from .session import ThreadsSession

TOOLS = [
    {
        "name": "threads_search_posts",
        "description": "Sub-80ms real-time keyword search across public Threads discussions without browser overhead or App Review",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search keyword or topic"},
                "limit": {"type": "integer", "default": 15, "description": "Max posts to return"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "threads_reply_post",
        "description": "Reply directly to any external Threads discussion (prohibited by official Graph API)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "parent_post_id": {"type": "string", "description": "Target thread post ID"},
                "text": {"type": "string", "description": "Reply text"},
                "reply_control": {"type": "string", "default": "everyone", "description": "everyone, accounts_you_follow, or mentioned_only"}
            },
            "required": ["parent_post_id", "text"]
        }
    },
    {
        "name": "threads_publish_post",
        "description": "Publish a new top-level text thread",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Thread post content"},
                "reply_control": {"type": "string", "default": "everyone", "description": "everyone, accounts_you_follow, or mentioned_only"}
            },
            "required": ["text"]
        }
    },
    {
        "name": "threads_get_discussion_tree",
        "description": "Extract full nested discussion tree (root post, parent, and all replies) for a post ID",
        "inputSchema": {
            "type": "object",
            "properties": {
                "post_id": {"type": "string", "description": "Target thread post ID"}
            },
            "required": ["post_id"]
        }
    },
    {
        "name": "threads_user_profile",
        "description": "Fetch user profile metadata by username or numeric user ID",
        "inputSchema": {
            "type": "object",
            "properties": {
                "username": {"type": "string", "description": "Target Threads username (optional if user_id is provided)"},
                "user_id": {"type": "string", "description": "Numeric user ID (optional if username is provided)"}
            }
        }
    },
    {
        "name": "threads_user_threads",
        "description": "Retrieve user's primary published threads feed",
        "inputSchema": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "Target user ID"},
                "max_id": {"type": "string", "description": "Pagination cursor"}
            },
            "required": ["user_id"]
        }
    },
    {
        "name": "threads_trending_topics",
        "description": "Fetch real-time trending topics and hashtags from Threads",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "threads_like_post",
        "description": "Like a Threads post",
        "inputSchema": {
            "type": "object",
            "properties": {
                "post_id": {"type": "string", "description": "Target thread post ID"}
            },
            "required": ["post_id"]
        }
    },
    {
        "name": "threads_repost",
        "description": "Repost / amplify a Threads post to followers",
        "inputSchema": {
            "type": "object",
            "properties": {
                "post_id": {"type": "string", "description": "Target thread post ID"}
            },
            "required": ["post_id"]
        }
    }
]

def _get_client() -> ThreadsAPI:
    api_key = os.getenv("THREADS_API_KEY", os.getenv("INSTAGRAM_API_KEY", ""))
    session_token = os.getenv("THREADS_SESSION_TOKEN", os.getenv("INSTAGRAM_SESSION_TOKEN"))
    device_preset = os.getenv("THREADS_DEVICE_PRESET", "threads_ios")
    session_path = os.getenv("THREADS_SESSION_FILE", "session_threads.json")

    session = None
    if os.path.exists(session_path):
        try:
            session = ThreadsSession.load_from_file(session_path)
        except Exception:
            session = None

    return ThreadsAPI(
        api_key=api_key,
        session=session,
        session_token=session_token,
        device_preset=device_preset,
    )

def handle_call_tool(name: str, arguments: dict) -> dict:
    threads = _get_client()
    try:
        if name == "threads_search_posts":
            posts = threads.search_posts(
                query=arguments["query"],
                limit=arguments.get("limit", 15),
            )
            data = [asdict(p) for p in posts]
            return {"content": [{"type": "text", "text": json.dumps(data, indent=2)}]}

        elif name == "threads_reply_post":
            res = threads.reply(
                parent_post_id=arguments["parent_post_id"],
                text=arguments["text"],
                reply_control=arguments.get("reply_control", "everyone"),
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

        elif name == "threads_publish_post":
            res = threads.content.publish_text(
                text=arguments["text"],
                reply_control=arguments.get("reply_control", "everyone"),
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

        elif name == "threads_get_discussion_tree":
            tree = threads.get_thread(post_id=arguments["post_id"])
            data = {
                "root_post": asdict(tree.root_post),
                "replies": [asdict(r) for r in tree.replies],
                "reply_count": len(tree.replies),
            }
            return {"content": [{"type": "text", "text": json.dumps(data, indent=2)}]}

        elif name == "threads_user_profile":
            if arguments.get("username"):
                res = threads.user.info_by_username(arguments["username"])
            elif arguments.get("user_id"):
                res = threads.user.info(arguments["user_id"])
            else:
                raise ValueError("Must provide either username or user_id")
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

        elif name == "threads_user_threads":
            res = threads.user.user_threads(
                user_id=arguments["user_id"],
                max_id=arguments.get("max_id"),
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

        elif name == "threads_trending_topics":
            res = threads.search.trending_topics()
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

        elif name == "threads_like_post":
            res = threads.like(post_id=arguments["post_id"])
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

        elif name == "threads_repost":
            res = threads.repost(post_id=arguments["post_id"])
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

        raise ValueError(f"Unknown tool: {name}")
    finally:
        threads.close()

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--list-tools":
        print(json.dumps(TOOLS, indent=2))
        return

    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            req_id = req.get("id")

            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "threads-private-api-mcp", "version": "1.0.0"}
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"tools": TOOLS}
                }
            elif method == "tools/call":
                params = req.get("params", {})
                result = handle_call_tool(params.get("name"), params.get("arguments", {}))
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": result
                }
            else:
                resp = {"jsonrpc": "2.0", "id": req_id, "result": {}}

            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32603, "message": str(e)}
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
