# Threads Protocol Architecture & Internals

Comprehensive technical overview of the reverse-engineered Threads (`com.instagram.barcelona`) protocol.

---

## 1. Meta Platform Lineage

Threads is built directly on Meta's Instagram infrastructure rather than a distinct backend stack. Under the hood:
- **Shared Gateway**: All mobile requests route through `https://i.instagram.com/api/v1/`.
- **Identity & Auth**: Bearer authorization headers format matches Instagram (`Authorization: Bearer IGT:2:<base64-payload>`). A valid Instagram session can be used interchangeably with Threads mobile endpoints.
- **Shared Social Graph**: Follows, blocks, mutes, and restrictions applied in Threads immediately reflect across Instagram and vice versa.

---

## 2. Protocol Transport Layers

```
                               +-------------------------------------+
                               |           threadsflow SDK           |
                               +------------------+------------------+
                                                  |
                         +------------------------+------------------------+
                         |                                                 |
                         v                                                 v
           +---------------------------+                     +---------------------------+
           |     Mobile REST API       |                     |     GraphQL Transport     |
           |   (Authenticated Ops)     |                     |    (Public Aggregation)   |
           +-------------+-------------+                     +-------------+-------------+
                         |                                                 |
                         v                                                 v
             i.instagram.com/api/v1/                            www.threads.net/api/graphql
           - Text thread publishing                           - Read-only thread lookups
           - External thread replies                          - High-throughput public search
           - Likes, reposts, user feed                        - Profile public extraction
```

### Layer A: Mobile REST Transport (`i.instagram.com/api/v1/`)
Primary interface for authenticated operations:
- Direct replies to external thread posts (`/api/v1/media/configure_text_post_app_feed/`)
- Publishing original posts (`/api/v1/media/configure_text_post_app_feed/`)
- Discussion tree retrieval (`/api/v1/text_post_app/{post_id}/text_post_app_thread/`)
- Real-time search (`/api/v1/fbsearch/topsearch_flat/?context=bloks_search`)
- Profile and user thread feeds (`/api/v1/text_post_app/{user_id}/profile/threads/`)

### Layer B: Persisted Query GraphQL (`www.threads.net/api/graphql`)
Used for ultra-high-throughput public thread monitoring without requiring authenticated sessions. Queries are executed via hash-persisted document IDs (`doc_id`).

---

## 3. Discussion Tree Structure

Unlike standard flat comment feeds, Threads organizes discussions into hierarchical recursive trees:

```
[Root Post / OP]
   |-- [Reply 1] (reply_to_post_id = root.id)
   |     |-- [Nested Reply 1.1] (reply_to_post_id = reply_1.id)
   |-- [Reply 2] (reply_to_post_id = root.id)
   |-- [Quote Post] (quoted_post_id = root.id)
```

The `DiscussionTree` model parses:
- `root_post`: Top-level thread item with author metadata, timestamp, text, media, and engagement counters.
- `replies`: List of child and grandchild replies flattened or traversed with parent-child linkage.

---

## 4. Sub-80ms Search & Trend Radar

The real-time discovery engine bypasses browser DOM parsing completely:
1. Dispatches HTTP/2 requests directly to `/api/v1/fbsearch/topsearch_flat/`.
2. Emulates native mobile Bloks search telemetry headers (`context=bloks_search`).
3. Wire-speed response serialization into native `ThreadPost` models under 80 milliseconds.
4. Operates over standard datacenter IPv4 / IPv6 IPs without triggering Cloudflare challenges.

---

## 5. Security & Antidetect Considerations

Meta applies lighter device-attestation checks to Threads traffic compared to Instagram web scrapers. However, to guarantee 99.9% uptime and zero checkpoint bans:
- Use consistent hardware profiles (do not flip between iOS and Android within the same session).
- Maintain authentic JA4 TLS 1.3 fingerprints (`t13d...` matching iOS Safari or Android OkHttp).
- Keep reply cadences within human-realistic boundaries (see [LICENSING_AND_LIMITS.md](LICENSING_AND_LIMITS.md)).
