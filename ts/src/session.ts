import * as fs from "fs";
import * as path from "path";
import { ThreadsSessionData } from "./types";

export class ThreadsSession {
  public sessionToken?: string;
  public devicePreset: string;
  public userId?: string;
  public cookies: Record<string, string>;

  constructor(sessionToken?: string, devicePreset: string = "threads_ios") {
    this.sessionToken = sessionToken;
    this.devicePreset = devicePreset;
    this.cookies = {};
  }

  public toDict(): ThreadsSessionData {
    return {
      sessionToken: this.sessionToken,
      devicePreset: this.devicePreset,
      userId: this.userId,
      cookies: this.cookies,
    };
  }

  public static fromDict(data: ThreadsSessionData): ThreadsSession {
    const session = new ThreadsSession(data.sessionToken, data.devicePreset || "threads_ios");
    session.userId = data.userId;
    session.cookies = data.cookies || {};
    return session;
  }

  public saveToFile(filePath: string): void {
    const dir = path.dirname(filePath);
    if (dir && !fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(filePath, JSON.stringify(this.toDict(), null, 2), "utf-8");
  }

  public static loadFromFile(filePath: string): ThreadsSession {
    const raw = fs.readFileSync(filePath, "utf-8");
    const parsed = JSON.parse(raw);
    return ThreadsSession.fromDict(parsed);
  }
}
