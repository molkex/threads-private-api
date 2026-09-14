/**
 * Error hierarchy for Threads private API client
 */

export class ThreadsError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ThreadsError";
  }
}

export class AuthError extends ThreadsError {
  constructor(message: string = "Threads authentication failed or session expired.") {
    super(message);
    this.name = "AuthError";
  }
}

export class ChallengeRequiredError extends ThreadsError {
  public challengeUrl?: string;

  constructor(message: string, challengeUrl?: string) {
    super(message);
    this.name = "ChallengeRequiredError";
    this.challengeUrl = challengeUrl;
  }
}

export class RateLimitError extends ThreadsError {
  constructor(message: string = "Threads rate limit (HTTP 429) encountered.") {
    super(message);
    this.name = "RateLimitError";
  }
}

export class PostNotFoundError extends ThreadsError {
  constructor(message: string = "Target thread post not found or was deleted.") {
    super(message);
    this.name = "PostNotFoundError";
  }
}

export class ServerError extends ThreadsError {
  public statusCode?: number;

  constructor(message: string, statusCode?: number) {
    super(message);
    this.name = "ServerError";
    this.statusCode = statusCode;
  }
}
