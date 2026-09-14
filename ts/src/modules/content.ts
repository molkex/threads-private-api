import { DiscussionTree, parseThreadPost } from "../types";

export interface IThreadsHttpClient {
  get(path: string, params?: Record<string, any>): Promise<any>;
  post(path: string, data?: Record<string, any>): Promise<any>;
}

export class ContentModule {
  private client: IThreadsHttpClient;

  constructor(client: IThreadsHttpClient) {
    this.client = client;
  }

  /**
   * Publish a new top-level text thread.
   * @param text Post content
   * @param replyControl 'everyone' | 'accounts_you_follow' | 'mentioned_only'
   */
  public async publishText(text: string, replyControl: string = "everyone"): Promise<any> {
    const data = {
      caption: text,
      text_post_app_info: JSON.stringify({ reply_control: replyControl }),
    };
    return this.client.post("/api/v1/media/configure_text_post_app_feed/", data);
  }

  /**
   * Reply directly to ANY public thread post without Meta App Review restrictions.
   * @param parentPostId Thread post ID
   * @param text Reply text
   * @param replyControl 'everyone' | 'accounts_you_follow' | 'mentioned_only'
   */
  public async reply(
    parentPostId: string | number,
    text: string,
    replyControl: string = "everyone",
  ): Promise<any> {
    const data = {
      caption: text,
      text_post_app_info: JSON.stringify({
        reply_to_post_id: String(parentPostId),
        reply_control: replyControl,
      }),
    };
    return this.client.post("/api/v1/media/configure_text_post_app_feed/", data);
  }

  /**
   * Quote an existing thread post with added commentary.
   */
  public async quote(quotedPostId: string | number, text: string): Promise<any> {
    const data = {
      caption: text,
      text_post_app_info: JSON.stringify({
        quoted_post_id: String(quotedPostId),
      }),
    };
    return this.client.post("/api/v1/media/configure_text_post_app_feed/", data);
  }

  /**
   * Retrieve complete nested discussion hierarchy (root post, parent, and recursive replies).
   */
  public async getThread(postId: string | number): Promise<DiscussionTree> {
    const res = await this.client.get(`/api/v1/text_post_app/${postId}/text_post_app_thread/`);
    const threadsData = res.containing_thread || res;
    const threadItems = threadsData.thread_items || [{}];
    const root = parseThreadPost(threadItems[0] || {});

    const replies = [];
    for (const item of res.reply_threads || []) {
      for (const tItem of item.thread_items || []) {
        replies.push(parseThreadPost(tItem));
      }
    }

    return {
      rootPost: root,
      replies,
      hasMore: Boolean(res.has_more),
      cursor: res.cursor,
    };
  }

  /**
   * Fetch list of accounts that liked this thread.
   */
  public async threadLikers(postId: string | number): Promise<any[]> {
    const res = await this.client.get(`/api/v1/media/${postId}/likers/`);
    return res.users || [];
  }

  /**
   * Like a thread post.
   */
  public async like(postId: string | number): Promise<any> {
    return this.client.post(`/api/v1/media/${postId}/like/`);
  }

  /**
   * Unlike a thread post.
   */
  public async unlike(postId: string | number): Promise<any> {
    return this.client.post(`/api/v1/media/${postId}/unlike/`);
  }

  /**
   * Repost / amplify a thread to your followers.
   */
  public async repost(postId: string | number): Promise<any> {
    return this.client.post(`/api/v1/media/${postId}/repost/`);
  }

  /**
   * Remove a previously reposted thread.
   */
  public async unrepost(postId: string | number): Promise<any> {
    return this.client.post(`/api/v1/media/${postId}/unrepost/`);
  }

  /**
   * Delete an owned thread post.
   */
  public async delete(postId: string | number): Promise<any> {
    const data = { media_id: String(postId) };
    return this.client.post(`/api/v1/media/${postId}/delete/`, data);
  }
}
