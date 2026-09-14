import { IThreadsHttpClient } from "./content";

export class UserModule {
  private client: IThreadsHttpClient;

  constructor(client: IThreadsHttpClient) {
    this.client = client;
  }

  /**
   * Fetch comprehensive user profile information by numeric user ID.
   */
  public async info(userId: string | number): Promise<any> {
    return this.client.get(`/api/v1/users/${userId}/info/`);
  }

  /**
   * Fetch user profile metadata by username.
   */
  public async infoByUsername(username: string): Promise<any> {
    return this.client.get(`/api/v1/users/${username}/usernameinfo/`);
  }

  /**
   * Retrieve user's primary published threads tab.
   */
  public async userThreads(userId: string | number, maxId?: string): Promise<any> {
    const params = maxId ? { max_id: maxId } : undefined;
    return this.client.get(`/api/v1/text_post_app/${userId}/profile/threads/`, params);
  }

  /**
   * Retrieve user's reply history tab.
   */
  public async userReplies(userId: string | number, maxId?: string): Promise<any> {
    const params = maxId ? { max_id: maxId } : undefined;
    return this.client.get(`/api/v1/text_post_app/${userId}/profile/replies/`, params);
  }

  /**
   * Retrieve user's reposted threads.
   */
  public async userReposts(userId: string | number, maxId?: string): Promise<any> {
    const params = maxId ? { max_id: maxId } : undefined;
    return this.client.get(`/api/v1/text_post_app/${userId}/profile/reposts/`, params);
  }

  /**
   * Search accounts by keyword or bio match.
   */
  public async searchUsers(query: string, limit: number = 10): Promise<any[]> {
    const params = {
      query,
      count: String(limit),
      context: "bloks_search_users",
    };
    const res = await this.client.get("/api/v1/fbsearch/topsearch_flat/", params);
    return res.list || [];
  }
}
