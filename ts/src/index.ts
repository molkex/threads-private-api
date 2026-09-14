/**
 * @molkex/threads-private-api
 * Modern, headless Threads (Barcelona) Mobile Private API SDK for TypeScript and Node.js
 */

export { ThreadsAPI, ThreadsClient } from "./client";
export { ThreadsSession } from "./session";
export { RemoteSigner, SignedRequestResult } from "./remote-signer";
export { THREADS_DEVICES, getThreadsDevice } from "./devices";

// Submodules
export { ContentModule, IThreadsHttpClient } from "./modules/content";
export { FeedModule } from "./modules/feed";
export { SearchModule } from "./modules/search";
export { SocialModule } from "./modules/social";
export { UserModule } from "./modules/user";

// Errors
export {
  ThreadsError,
  AuthError,
  ChallengeRequiredError,
  RateLimitError,
  PostNotFoundError,
  ServerError,
} from "./errors";

// Types & Parsers
export {
  ThreadAuthor,
  ThreadPost,
  DiscussionTree,
  ThreadsDevicePreset,
  ThreadsSessionData,
  ThreadsClientOptions,
  parseThreadAuthor,
  parseThreadPost,
} from "./types";
