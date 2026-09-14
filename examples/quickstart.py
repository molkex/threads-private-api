"""
Example: Headless Threads keyword search, discussion tree scraping & auto-reply.
"""
from threadsflow import ThreadsAPI, ThreadsSession

def main():
    # 1. Real-time keyword discovery (zero proxy cost, sub-80ms)
    threads = ThreadsAPI(device_preset="threads_ios")
    print("Searching public discussions for keyword 'ai agents'...")
    posts = threads.search_posts(query="ai agents", limit=5)
    for post in posts:
        print(f"[@{post.author.username}] ({post.like_count} likes): {post.caption[:80]}...")
        print(f"Post ID: {post.id} | Code: {post.code}")

    # 2. Authenticated replies (using shared Meta session)
    # session = ThreadsSession.load_from_file("session_threads.json")
    # auth_client = ThreadsAPI(session=session)
    # auth_client.reply(parent_post_id="3141592653589793238", text="Great perspective!")

if __name__ == "__main__":
    main()
