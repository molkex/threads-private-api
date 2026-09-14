# Autonomous Agent Integration Guide for Threads

This document instructs AI coding assistants (Claude Desktop, Cursor, Windsurf, Antigravity) how to interact with `threadsflow` and `@molkex/threads-private-api`.

---

## Running as an MCP Server

The package includes a built-in Model Context Protocol server.

### Claude Desktop / Cursor Configuration

Add the following to your `claude_desktop_config.json` or Cursor MCP settings:

```json
{
  "mcpServers": {
    "threads": {
      "command": "python",
      "args": ["-m", "threadsflow.mcp_server"],
      "env": {
        "THREADS_API_KEY": "your_api_key_here",
        "THREADS_SESSION_FILE": "session_threads.json",
        "THREADS_DEVICE_PRESET": "threads_ios"
      }
    }
  }
}
```

---

## Agent Tool Reference

| Tool Name | Purpose | Required Arguments |
|:---|:---|:---|
| `threads_search_posts` | Search public Threads discussions in real time (<80ms) | `query` (string) |
| `threads_get_discussion_tree` | Retrieve full nested discussion tree (root post + recursive replies) | `post_id` (string) |
| `threads_reply_post` | Reply directly to any external thread post without Meta App Review | `parent_post_id`, `text` |
| `threads_publish_post` | Publish a new top-level text thread | `text` |
| `threads_user_profile` | Fetch profile metadata for a user | `username` or `user_id` |
| `threads_user_threads` | Fetch recent published threads by user | `user_id` |
| `threads_trending_topics` | Fetch trending topics and hashtags | None |
| `threads_like_post` | Like a thread post | `post_id` |
| `threads_repost` | Repost / amplify a thread | `post_id` |

---

## Common Agent Workflows

### 1. Market Research & Sentiment Analysis
1. Call `threads_search_posts(query="your product or topic")`.
2. Inspect post content, engagement counters (`likeCount`, `replyCount`).
3. Call `threads_get_discussion_tree(post_id=...)` on top posts to read nested community feedback.

### 2. Targeted Community Engagement
1. Call `threads_search_posts(query="seeking advice on ...")`.
2. Select high-relevance posts with active discussions.
3. Call `threads_reply_post(parent_post_id=..., text="Helpful advice...")`.
