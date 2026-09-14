import { ThreadPost, parseThreadPost } from "../types";
import { IThreadsHttpClient } from "./content";

export class SearchModule {
  private client: IThreadsHttpClient;

  constructor(client: IThreadsHttpClient) {
    this.client = client;
  }

  /**
   * Sub-80ms wire-speed keyword search across public Threads discussions.
   * No browser rendering, no official App Review limitation.
   */
  public async searchPosts(query: string, limit: number = 15): Promise<ThreadPost[]> {
    const params = {
      query,
      count: String(limit),
      context: "bloks_search",
    };
    const res = await this.client.get("/api/v1/fbsearch/topsearch_flat/", params);
    const posts: ThreadPost[] = [];

    for (const item of res.list || []) {
      const thread = item.thread || item;
      if (thread) {
        posts.push(parseThreadPost(thread));
      }
    }
    return posts;
  }

  /**
   * Fetch real-time trending topics, hashtags, and viral discussion prompts.
   */
  public async trendingTopics(): Promise<any[]> {
    const res = await this.client.get("/api/v1/text_post_app/trending_topics/");
    return res.trending_topics || res.items || [];
  }
}
