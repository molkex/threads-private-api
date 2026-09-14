import {
  ThreadsClientOptions,
  ThreadsDevicePreset,
  ThreadPost,
  DiscussionTree,
} from "./types";
import { getThreadsDevice } from "./devices";
import { RemoteSigner } from "./remote-signer";
import { ThreadsSession } from "./session";
import { AuthError, RateLimitError, ServerError } from "./errors";
import { ContentModule, IThreadsHttpClient } from "./modules/content";
import { FeedModule } from "./modules/feed";
import { SearchModule } from "./modules/search";
import { SocialModule } from "./modules/social";
import { UserModule } from "./modules/user";

export class ThreadsAPI implements IThreadsHttpClient {
  public static readonly BASE_URL = "https://i.instagram.com";

  public apiKey: string;
  public sessionToken?: string;
  public session?: ThreadsSession;
  public devicePreset: string;
  public device: ThreadsDevicePreset;
  public signer: RemoteSigner;

  public user: UserModule;
  public content: ContentModule;
  public feed: FeedModule;
  public search: SearchModule;
  public social: SocialModule;

  constructor(options: ThreadsClientOptions & { session?: ThreadsSession } = {}) {
    this.apiKey = options.apiKey || "";
    this.session = options.session;

    if (this.session) {
      if (this.session.sessionToken && !options.sessionToken) {
        options.sessionToken = this.session.sessionToken;
      }
      if (this.session.devicePreset && !options.devicePreset) {
        options.devicePreset = this.session.devicePreset;
      }
    }

    this.sessionToken = options.sessionToken;
    this.devicePreset = options.devicePreset || "threads_ios";
    this.device = getThreadsDevice(this.devicePreset);
    this.signer = new RemoteSigner(
      options.signingServer || "http://127.0.0.1:8643",
      this.apiKey,
      this.devicePreset,
    );

    this.user = new UserModule(this);
    this.content = new ContentModule(this);
    this.feed = new FeedModule(this);
    this.search = new SearchModule(this);
    this.social = new SocialModule(this);
  }

  /**
   * Sub-80ms real-time keyword search across public Threads discussions.
   */
  public async searchPosts(query: string, limit: number = 15): Promise<ThreadPost[]> {
    return this.search.searchPosts(query, limit);
  }

  /**
   * Reply directly to any external thread post without Meta App Review restrictions.
   */
  public async reply(
    parentPostId: string | number,
    text: string,
    replyControl: string = "everyone",
  ): Promise<any> {
    return this.content.reply(parentPostId, text, replyControl);
  }

  /**
   * Like a thread post.
   */
  public async like(postId: string | number): Promise<any> {
    return this.content.like(postId);
  }

  /**
   * Repost / amplify a thread.
   */
  public async repost(postId: string | number): Promise<any> {
    return this.content.repost(postId);
  }

  /**
   * Extract full nested discussion tree with replies.
   */
  public async getThread(postId: string | number): Promise<DiscussionTree> {
    return this.content.getThread(postId);
  }

  public async get(path: string, params?: Record<string, any>): Promise<any> {
    const signed = await this.signer.signRequest(path, "GET");
    const headers: Record<string, string> = { ...signed.headers };
    if (this.sessionToken) {
      headers["Authorization"] = `Bearer ${this.sessionToken}`;
    }

    let url = `${ThreadsAPI.BASE_URL}${path}`;
    if (params && Object.keys(params).length > 0) {
      const searchParams = new URLSearchParams();
      for (const [k, v] of Object.entries(params)) {
        if (v !== undefined && v !== null) {
          searchParams.append(k, String(v));
        }
      }
      url += (url.includes("?") ? "&" : "?") + searchParams.toString();
    }

    const resp = await fetch(url, { method: "GET", headers });
    return this.handleResponse(resp);
  }

  public async post(path: string, data?: Record<string, any>): Promise<any> {
    const signed = await this.signer.signRequest(path, "POST", data);
    const headers: Record<string, string> = { ...signed.headers };
    if (this.sessionToken) {
      headers["Authorization"] = `Bearer ${this.sessionToken}`;
    }

    const payload = signed.signed_body || data || {};
    const bodyParams = new URLSearchParams();
    for (const [k, v] of Object.entries(payload)) {
      if (v !== undefined && v !== null) {
        bodyParams.append(k, typeof v === "object" ? JSON.stringify(v) : String(v));
      }
    }

    const resp = await fetch(`${ThreadsAPI.BASE_URL}${path}`, {
      method: "POST",
      headers,
      body: bodyParams.toString(),
    });
    return this.handleResponse(resp);
  }

  private async handleResponse(resp: Response): Promise<any> {
    if (resp.status === 401) {
      throw new AuthError("Threads authentication failed or session expired.");
    }
    if (resp.status === 429) {
      throw new RateLimitError("Threads rate limit (429) encountered.");
    }
    if (resp.status >= 500) {
      throw new ServerError(`Threads server error: ${resp.status}`, resp.status);
    }
    try {
      return await resp.json();
    } catch {
      const text = await resp.text();
      return { status: "ok", statusCode: resp.status, text: text.slice(0, 200) };
    }
  }

  public close(): void {
    // No-op for fetch-based client
  }
}

// Friendly alias
export const ThreadsClient = ThreadsAPI;
