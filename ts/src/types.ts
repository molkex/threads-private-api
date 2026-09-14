/**
 * Type definitions for @molkex/threads-private-api
 */

export interface ThreadAuthor {
  pk: number;
  username: string;
  fullName: string;
  profilePicUrl: string;
  isVerified: boolean;
}

export interface ThreadPost {
  id: string;
  pk: number;
  code: string;
  caption: string;
  author: ThreadAuthor;
  likeCount: number;
  replyCount: number;
  repostCount: number;
  takenAt: number;
  replyToPostId?: string;
  mediaType: number;
}

export interface DiscussionTree {
  rootPost: ThreadPost;
  replies: ThreadPost[];
  hasMore?: boolean;
  cursor?: string;
}

export interface ThreadsDevicePreset {
  name: string;
  platform: "iOS" | "Android" | "Web";
  appId: string;
  bloksVersionId: string;
  capabilities: string;
  userAgent: string;
  appVersion: string;
  deviceModel: string;
}

export interface ThreadsSessionData {
  sessionToken?: string;
  devicePreset?: string;
  userId?: string;
  cookies?: Record<string, string>;
}

export interface ThreadsClientOptions {
  apiKey?: string;
  sessionToken?: string;
  signingServer?: string;
  devicePreset?: "threads_ios" | "threads_android" | "threads_web" | string;
  proxy?: string;
  timeoutMs?: number;
}

export function parseThreadAuthor(user: any = {}): ThreadAuthor {
  return {
    pk: Number(user.pk || 0),
    username: String(user.username || ""),
    fullName: String(user.full_name || ""),
    profilePicUrl: String(user.profile_pic_url || ""),
    isVerified: Boolean(user.is_verified || false),
  };
}

export function parseThreadPost(item: any = {}): ThreadPost {
  const thread = item.thread || item;
  const captionObj = thread.caption || {};
  const captionText = typeof captionObj === "object" ? String(captionObj.text || "") : String(captionObj);
  const userObj = thread.user || {};

  return {
    id: String(thread.id || thread.pk || ""),
    pk: Number(thread.pk || thread.id || 0),
    code: String(thread.code || ""),
    caption: captionText,
    author: parseThreadAuthor(userObj),
    likeCount: Number(thread.like_count || 0),
    replyCount: Number(thread.reply_count || 0),
    repostCount: Number(thread.repost_count || 0),
    takenAt: Number(thread.taken_at || 0),
    replyToPostId: thread.reply_to_post_id ? String(thread.reply_to_post_id) : undefined,
    mediaType: Number(thread.media_type || 1),
  };
}

