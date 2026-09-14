import { ThreadsDevicePreset } from "./types";

export const THREADS_DEVICES: Record<string, ThreadsDevicePreset> = {
  threads_ios: {
    name: "Threads iOS (iPhone 15 Pro)",
    platform: "iOS",
    appId: "1546306509211461",
    bloksVersionId: "95cbfdb413e12cf21841dcfd299719b165f658155182b7989fd661be5ea52089",
    capabilities: "36r/F/8=",
    userAgent: "Barcelona 410.2.0.33.71 (iPhone16,1; iOS 17_6_1; en_US; en-US; scale=3.00; 1179x2556; 850146623) AppleWebKit/420+",
    appVersion: "410.2.0.33.71",
    deviceModel: "iPhone 15 Pro",
  },
  threads_android: {
    name: "Threads Android (Samsung Galaxy A34 / S24)",
    platform: "Android",
    appId: "3419628305025917",
    bloksVersionId: "95cbfdb413e12cf21841dcfd299719b165f658155182b7989fd661be5ea52089",
    capabilities: "3brTv10=",
    userAgent: "Barcelona 410.2.0.33.71 Android (34/14; 450dpi; 1080x2400; samsung; SM-A346B; a34x; mt6877; en_US; 850146623)",
    appVersion: "410.2.0.33.71",
    deviceModel: "Samsung Galaxy A34 5G",
  },
  threads_web: {
    name: "Threads Web Public GraphQL",
    platform: "Web",
    appId: "238260118697367",
    bloksVersionId: "95cbfdb413e12cf21841dcfd299719b165f658155182b7989fd661be5ea52089",
    capabilities: "36r/F/8=",
    userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    appVersion: "410.2.0.33.71",
    deviceModel: "Desktop Web",
  },
};

export function getThreadsDevice(presetKey: string = "threads_ios"): ThreadsDevicePreset {
  const key = presetKey.toLowerCase().replace(/-/g, "_");
  if (key.includes("android") || key.includes("samsung") || key.includes("pixel") || key.includes("galaxy")) {
    return THREADS_DEVICES.threads_android;
  }
  if (key.includes("web")) {
    return THREADS_DEVICES.threads_web;
  }
  return THREADS_DEVICES.threads_ios;
}
