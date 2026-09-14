# Licensing, Rate Limits & Account Safety

Guidance on production rate limits, account safety margins, and enterprise licensing for Threads.

---

## 1. Action Velocity Limits (Per Account)

Threads shares trust scores with Instagram. To avoid temporary action blocks or automated behavior warnings, respect the following velocity ceilings:

| Action | New / Warmed < 14 Days | Aged / Established Account | Recommended Sleep Interval |
|:---|:---|:---|:---|
| **Real-Time Keyword Search** | Unlimited (Read-only) | Unlimited (Read-only) | 0.5 - 2s |
| **Discussion Tree Scraping** | Unlimited (Read-only) | Unlimited (Read-only) | 0.5 - 2s |
| **External Thread Replies** | 10 - 20 / day | 60 - 120 / day | 45 - 120s between replies |
| **Thread Likes** | 30 - 50 / day | 150 - 250 / day | 15 - 45s between likes |
| **Reposts** | 10 - 20 / day | 50 - 80 / day | 30 - 60s between reposts |
| **Top-Level Posts** | 3 - 6 / day | 10 - 20 / day | Human pacing |

---

## 2. Preventing Automated Behavior Warnings

1. **Vary Reply Content**: Never send identical reply strings repeatedly. Use dynamic LLM generation with temperature > 0.7.
2. **Organic Timeline Activity**: Interleave reply activity with timeline reads (`client.feed.timeline()`) and likes.
3. **Session Persistence**: Do not log in from scratch on every run. Save and restore sessions via `ThreadsSession`.
4. **IP Consistency**: Pin an account to a consistent residential or high-quality static proxy IP.

---

## 3. Commercial Licensing & Custom Infrastructure

For high-throughput keyword radar clusters, real-time brand mention webhooks, or multi-account reply fleets:

- **Contact**: [@mxmtkchk](https://t.me/mxmtkchk) on Telegram
- **Enterprise Features**:
  - Distributed multi-account rotation engine
  - Real-time Kafka / Webhook event stream for new keywords
  - Automated SMS/Email challenge solving daemon
  - Dedicated signing cluster with 99.99% SLA
