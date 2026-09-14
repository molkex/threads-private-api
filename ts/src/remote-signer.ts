import { ThreadsDevicePreset } from "./types";
import { getThreadsDevice } from "./devices";
import { AuthError, ServerError } from "./errors";

export interface SignedRequestResult {
  headers: Record<string, string>;
  signed_body?: Record<string, any>;
}

export class RemoteSigner {
  public signingServer: string;
  public apiKey: string;
  public devicePreset: string;
  public device: ThreadsDevicePreset;

  constructor(
    signingServer: string = "http://127.0.0.1:8643",
    apiKey: string = "",
    devicePreset: string = "threads_ios",
  ) {
    this.signingServer = signingServer.replace(/\/+$/, "");
    this.apiKey = apiKey;
    this.devicePreset = devicePreset;
    this.device = getThreadsDevice(devicePreset);
  }

  public async signRequest(
    endpoint: string,
    method: string = "POST",
    body?: Record<string, any>,
  ): Promise<SignedRequestResult> {
    const payload = {
      api_key: this.apiKey,
      device_preset: this.devicePreset,
      endpoint,
      method: method.toUpperCase(),
      platform: "threads",
      body: body || {},
    };

    try {
      const resp = await fetch(`${this.signingServer}/v1/sign`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (resp.status === 401 || resp.status === 403) {
        throw new AuthError("Threads signing authorization failed. Valid API key required.");
      }
      if (resp.status >= 500) {
        throw new ServerError(`Signing daemon error: ${resp.status}`, resp.status);
      }
      return (await resp.json()) as SignedRequestResult;
    } catch (err: any) {
      if (err instanceof AuthError || err instanceof ServerError) {
        throw err;
      }
      return this.fallbackLocalSign(endpoint, method, body);
    }
  }

  public fallbackLocalSign(
    _endpoint: string,
    _method: string,
    body?: Record<string, any>,
  ): SignedRequestResult {
    const headers: Record<string, string> = {
      "User-Agent": this.device.userAgent,
      "X-IG-App-ID": this.device.appId,
      "X-Bloks-Version-Id": this.device.bloksVersionId,
      "X-IG-Capabilities": this.device.capabilities,
      "X-IG-Connection-Type": "WIFI",
      "Accept-Language": "en-US,en;q=0.9",
      "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    };

    return {
      headers,
      signed_body: body || {},
    };
  }
}
