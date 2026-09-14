# Threads Hardware & Network Fingerprints

Threads enforces mobile platform headers and capabilities. Below are the verified device profiles used by `threadsflow`.

---

## 1. Threads iOS Preset (`threads_ios`)

Based on Apple iPhone 15 Pro running iOS 17.6.1:

| Field | Value |
|:---|:---|
| **App ID (`X-IG-App-ID`)** | `1546306509211461` |
| **Bloks Version ID** | `95cbfdb413e12cf21841dcfd299719b165f658155182b7989fd661be5ea52089` |
| **Capabilities** | `36r/F/8=` |
| **App Version** | `410.2.0.33.71` |
| **User Agent** | `Barcelona 410.2.0.33.71 (iPhone16,1; iOS 17_6_1; en_US; en-US; scale=3.00; 1179x2556; 850146623) AppleWebKit/420+` |
| **Connection Type** | `WIFI` |
| **Accept-Language** | `en-US,en;q=0.9` |

---

## 2. Threads Android Preset (`threads_android`)

Based on Samsung Galaxy A34 5G running Android 14:

| Field | Value |
|:---|:---|
| **App ID (`X-IG-App-ID`)** | `3419628305025917` |
| **Bloks Version ID** | `95cbfdb413e12cf21841dcfd299719b165f658155182b7989fd661be5ea52089` |
| **Capabilities** | `3brTv10=` |
| **App Version** | `410.2.0.33.71` |
| **User Agent** | `Barcelona 410.2.0.33.71 Android (34/14; 450dpi; 1080x2400; samsung; SM-A346B; a34x; mt6877; en_US; 850146623)` |
| **Connection Type** | `WIFI` |
| **Accept-Language** | `en-US,en;q=0.9` |

---

## 3. Public Web GraphQL Preset (`threads_web`)

Used for unauthenticated read-only scraping:

| Field | Value |
|:---|:---|
| **App ID (`X-IG-App-ID`)** | `238260118697367` |
| **Endpoint Host** | `www.threads.net` |
| **User Agent** | Standard modern Chrome / Safari Desktop UA |

---

## 4. Header Synchronization

When sending mobile REST requests, the following headers are synchronized automatically by the client:

```http
User-Agent: Barcelona 410.2.0.33.71 (iPhone16,1; iOS 17_6_1; en_US; en-US; scale=3.00; 1179x2556; 850146623) AppleWebKit/420+
X-IG-App-ID: 1546306509211461
X-Bloks-Version-Id: 95cbfdb413e12cf21841dcfd299719b165f658155182b7989fd661be5ea52089
X-IG-Capabilities: 36r/F/8=
X-IG-Connection-Type: WIFI
Accept-Language: en-US,en;q=0.9
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Authorization: Bearer <token>
```
