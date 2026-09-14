import { IThreadsHttpClient } from "./content";

export class SocialModule {
  private client: IThreadsHttpClient;

  constructor(client: IThreadsHttpClient) {
    this.client = client;
  }

  /**
   * Follow user (reflects across both Threads and Instagram).
   */
  public async follow(userId: string | number): Promise<any> {
    return this.client.post(`/api/v1/friendships/create/${userId}/`);
  }

  /**
   * Unfollow user.
   */
  public async unfollow(userId: string | number): Promise<any> {
    return this.client.post(`/api/v1/friendships/destroy/${userId}/`);
  }

  /**
   * Block user.
   */
  public async block(userId: string | number): Promise<any> {
    return this.client.post(`/api/v1/friendships/block/${userId}/`);
  }

  /**
   * Unblock user.
   */
  public async unblock(userId: string | number): Promise<any> {
    return this.client.post(`/api/v1/friendships/unblock/${userId}/`);
  }

  /**
   * Mute posts from user.
   */
  public async mute(userId: string | number): Promise<any> {
    const data = { target_posts_author_id: String(userId) };
    return this.client.post("/api/v1/friendships/mute_posts_or_story_from_follow/", data);
  }

  /**
   * Unmute posts from user.
   */
  public async unmute(userId: string | number): Promise<any> {
    const data = { target_posts_author_id: String(userId) };
    return this.client.post("/api/v1/friendships/unmute_posts_or_story_from_follow/", data);
  }

  /**
   * Restrict user interaction.
   */
  public async restrict(userId: string | number): Promise<any> {
    return this.client.post("/api/v1/restrict_action/restrict_user/", { target_user_id: String(userId) });
  }

  /**
   * Unrestrict user.
   */
  public async unrestrict(userId: string | number): Promise<any> {
    return this.client.post("/api/v1/restrict_action/unrestrict_user/", { target_user_id: String(userId) });
  }
}
