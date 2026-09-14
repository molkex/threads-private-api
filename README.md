# threads-private-api

**Unofficial Threads Private API & Trend Radar SDK for Python and TypeScript.**
High-performance headless protocol engine for Threads (`com.instagram.barcelona`). Sub-80ms real-time keyword search, full nested discussion tree ingestion, external thread replies, and zero residential proxy cost.

[![Ingestion: Sub-80ms Ingestion](https://img.shields.io/badge/Latency-Sub--80ms%20Ingestion-10b981.svg)](#)
[![TypeScript: Full Types](https://img.shields.io/badge/TypeScript-Ready-3178c6.svg)](#)
[![Python: >=3.10](https://img.shields.io/badge/Python->=3.10-3776ab.svg)](#)
[![Proxies: Zero Residential Needed](https://img.shields.io/badge/Proxies-Zero%20Residential%20Needed-0f172a.svg)](#)
[![Protocol: GraphQL & Mobile REST](https://img.shields.io/badge/Protocol-GraphQL%20%26%20Mobile%20REST-2563eb.svg)](#)
[![Telegram Contact](https://img.shields.io/badge/Telegram-@mxmtkchk-229ED9.svg)](https://t.me/mxmtkchk)

> **Companion Project**: Looking for full Instagram mobile automation, DM outreach, warmup loops, and Reels publishing?
> Check out [instagram-private-api](https://github.com/molkex/instagram-private-api) — Pure HTTP/2 zero-device engine with authentic Android 14 / iOS 17 JA4 TLS 1.3 signatures.

---

## Why this instead of Official Threads API or Playwright

| Feature | Official Threads API (`graph.threads.net`) | Browser Scraping (Playwright / Puppeteer) | threads-private-api SDK |
|:---|:---|:---|:---|
| **Meta App Review** | Mandatory (Tech Provider status required) | Not needed | **Not needed** |
| **Search Public Threads** | Restricted / Closed to public apps | High latency DOM parsing | **Direct Sub-80ms Real-Time Search** |
| **Reply to External Threads** | Impossible (Only own threads allowed) | Brittle DOM selectors & high ban risk | **Native Protocol Direct Reply** |
| **Nested Discussion Trees** | Limited pagination | Unstable infinite scroll rendering | **Full Recursive Comment Hierarchy** |
| **RAM per Worker** | Minimal (Cloud API) | 2 - 4 GB per browser instance | **< 60 MB** |
| **Residential Proxy Need** | None | Mandatory (Aggressive Cloudflare/Bot IP bans) | **Standard Datacenter / IPv6 Compatible** |
| **Execution Latency** | 250 - 600 ms | 3,000 - 8,000 ms | **35 - 80 ms** |

---

## Key Highlights

- **Direct Reply to Any External Thread**: The official Graph API strictly blocks replying to threads created by other accounts. This SDK uses native mobile protocol endpoints to discover any thread's internal media ID and dispatch replies directly.
- **Sub-80ms Real-Time Ingestion**: Query keyword streams, emerging topics, and brand mentions at wire speed without browser overhead.
- **Full Nested Reply Trees**: Traverses complex multi-level conversations, quotes, parent-child comments, and author engagement metadata.
- **Dual Platform Hardware Presets**:
  - **Threads iOS**: `Barcelona 410.2.0.33.71 (iPhone16,1; iOS 17_6_1)`, `X-IG-App-ID: 1546306509211461`.
  - **Threads Android**: `Barcelona 410.2.0.33.71 Android (34/14; Samsung SM-A346B)`, `X-IG-App-ID: 3419628305025917`.
- **Unified Meta Auth**: Shares the identical bearer token format with Instagram (`Authorization: Bearer IGT:2:...`). Drive both platforms using a single unified session.
- **Shared Social Graph**: Follows, unfollows, and block states automatically reflect across both Instagram and Threads.

---

## Installation

### Python
```bash
git clone https://github.com/molkex/threads-private-api.git
cd threads-private-api
pip install -e .
```

### TypeScript / Node.js
```bash
cd ts
npm install
npm run build
```

---

## Quickstart (Python)

### 1. Real-Time Keyword Search (<80ms)

```python
from threadsflow import ThreadsAPI

# Unauthenticated public discovery or authenticated session
threads = ThreadsAPI(device_preset="threads_ios")

# Search public discussions in real-time
posts = threads.search_posts(query="ai agents", limit=15)

for post in posts:
    print(f"[@{post.author.username}] ({post.like_count} likes): {post.caption[:80]}...")
    print(f"Post ID: {post.id} | Code: {post.code}")
```

### 2. Reading Nested Discussion Trees & Replying to External Threads

```python
from threadsflow import ThreadsAPI, ThreadsSession

# Load session
session = ThreadsSession.load_from_file("session_threads.json")
threads = ThreadsAPI(session=session)

# Ingest complete nested discussion tree
tree = threads.get_thread(post_id="3141592653589793238")
print(f"Root OP by @{tree.root_post.author.username}: {tree.root_post.caption}")

for reply in tree.replies:
    print(f"-> @{reply.author.username}: {reply.caption}")

# Reply directly to ANY public thread post (prohibited in official Graph API)
res = threads.reply(
    parent_post_id="3141592653589793238",
    text="Great perspective! We solved this with headless HTTP/2 protocol emulation."
)
print("Reply sent successfully:", res.get("status"))
```

### 3. Publishing New Posts & Engagement

```python
# Publish top-level text thread
post = threads.content.publish_text(
    text="Deploying sub-80ms real-time trend radar for Threads today."
)

# Like and repost
threads.like(post_id="3141592653589793238")
threads.repost(post_id="3141592653589793238")
```

---

## Quickstart (TypeScript / Node.js)

```typescript
import { ThreadsAPI, ThreadsSession } from "@molkex/threads-private-api";

async function run() {
  const threads = new ThreadsAPI({ devicePreset: "threads_ios" });

  // 1. Sub-80ms search
  const posts = await threads.searchPosts("open source", 10);
  for (const post of posts) {
    console.log(`[@${post.author.username}] ${post.caption.slice(0, 70)}...`);
  }

  // 2. Fetch full discussion hierarchy
  const tree = await threads.getThread("3141592653589793238");
  console.log(`Root: ${tree.rootPost.caption}`);
  console.log(`Replies count: ${tree.replies.length}`);

  // 3. Direct reply (authenticated)
  // const session = ThreadsSession.loadFromFile("session_threads.json");
  // const authThreads = new ThreadsAPI({ session });
  // await authThreads.reply("3141592653589793238", "Excellent breakdown!");
}

run();
```

---

## Model Context Protocol (MCP) Server

AI agents (Claude Desktop, Cursor, Windsurf, Antigravity) can use Threads tools directly via the built-in MCP server:

```bash
python -m threadsflow.mcp_server
```

Tools exposed:
- `threads_search_posts`: Sub-80ms real-time keyword search
- `threads_get_discussion_tree`: Extract complete nested discussion tree
- `threads_reply_post`: Reply directly to any external thread post
- `threads_publish_post`: Publish new top-level thread
- `threads_user_profile`: Fetch user profile by ID or username
- `threads_user_threads`: Retrieve user thread feed
- `threads_trending_topics`: Fetch real-time trending topics
- `threads_like_post`: Like post
- `threads_repost`: Repost / amplify post

See [AGENT_GUIDE.md](AGENT_GUIDE.md) for full agent configuration.

---

## Endpoint Modules

| Module | Methods & Capabilities |
|:---|:---|
| `th.content` | `publish_text`, `reply`, `quote`, `repost`, `unrepost`, `like`, `unlike`, `delete`, `get_thread`, `thread_likers` |
| `th.search` | `search_posts` (<80ms wire-speed), `trending_topics` |
| `th.user` | `info`, `info_by_username`, `user_threads`, `user_replies`, `user_reposts`, `search_users` |
| `th.social` | `follow`, `unfollow`, `block`, `unblock`, `mute`, `unmute`, `restrict`, `unrestrict` (shared Instagram social graph) |
| `th.feed` | `timeline`, `following_timeline`, `notifications`, `set_notifications_seen` |

---

## Technical Documentation

- [Architecture & Protocol Internals](docs/ARCHITECTURE.md)
- [Hardware & Network Fingerprints](docs/HARDWARE_FINGERPRINTS.md)
- [Licensing, Rate Limits & Safety Margins](docs/LICENSING_AND_LIMITS.md)
- [Autonomous Agent Guide](AGENT_GUIDE.md)

---

## Licensing & Enterprise Access

Private builds, cluster deployment packages, and custom scrapers are available for growth teams, PR monitoring platforms, and automation agencies.

- **Direct Inquiries**: [@mxmtkchk](https://t.me/mxmtkchk) on Telegram
- **Enterprise Features**:
  - Continuous persisted GraphQL doc_id synchronization service
  - Real-time keyword webhook daemon
  - High-throughput multi-account reply clusters
  - Custom data pipeline integration (Postgres, ClickHouse, Kafka)

For questions, pricing plans, and integration support, contact **[@mxmtkchk](https://t.me/mxmtkchk)** on Telegram.

---

## Disclaimer

This repository is provided for educational and reverse-engineering research purposes only. Not affiliated with, authorized, or endorsed by Threads, Instagram, or Meta Platforms, Inc. Use responsibly and in accordance with applicable platform policies and legal requirements.
