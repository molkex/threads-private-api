/**
 * Quickstart: Headless Threads keyword discovery and discussion tree inspection.
 */
import { ThreadsAPI, ThreadsSession } from "../src";

async function main() {
  // 1. Unauthenticated or session-based client
  const threads = new ThreadsAPI({
    devicePreset: "threads_ios",
  });

  console.log("Searching public discussions for 'ai agents'...");
  const posts = await threads.searchPosts("ai agents", 5);

  for (const post of posts) {
    console.log(`[@${post.author.username}] (${post.likeCount} likes): ${post.caption.slice(0, 80)}...`);
    console.log(`Post ID: ${post.id} | Code: ${post.code}`);
  }

  // 2. Fetch full discussion tree
  if (posts.length > 0) {
    const targetId = posts[0].id;
    console.log(`\nFetching discussion tree for post ${targetId}...`);
    const tree = await threads.getThread(targetId);
    console.log(`Root OP by @${tree.rootPost.author.username}: ${tree.rootPost.caption}`);
    console.log(`Found ${tree.replies.length} replies.`);
  }

  // 3. Authenticated session reply example
  // const session = ThreadsSession.loadFromFile("session_threads.json");
  // const authClient = new ThreadsAPI({ session });
  // await authClient.reply("3141592653589793238", "Great perspective on headless architecture!");
}

main().catch(console.error);
