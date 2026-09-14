import { IThreadsHttpClient } from "./content";

export class FeedModule {
  private client: IThreadsHttpClient;

  constructor(client: IThreadsHttpClient) {
    this.client = client;
  }

  /**
   * Fetch recommended 'For You' Threads timeline feed.
   */
  public async timeline(maxId?: string): Promise<any> {
    const params = maxId ? { max_id: maxId } : undefined;
    return this.client.get("/api/v1/feed/text_post_app_timeline/", params);
  }

  /**
   * Fetch chronological 'Following' timeline feed.
   */
  public async followingTimeline(maxId?: string): Promise<any> {
    const params = maxId ? { max_id: maxId } : undefined;
    return this.client.get("/api/v1/feed/text_post_app_following_timeline/", params);
  }

  /**
   * Fetch activity notifications (replies, mentions, quotes, likes).
   */
  public async notifications(filterType?: string): Promise<any> {
    const params = filterType ? { filter_type: filterType } : undefined;
    return this.client.get("/api/v1/text_post_app/news_feed/", params);
  }

  /**
   * Mark all incoming activity notifications as seen.
   */
  public async setNotificationsSeen(): Promise<any> {
    return this.client.post("/api/v1/text_post_app/news_feed_seen/");
  }
}
