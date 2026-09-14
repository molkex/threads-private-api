"""
Hardware and network profile presets for Threads (com.instagram.barcelona).
Dual iOS and Android mobile stack emulation.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class ThreadsDevicePreset:
    name: str
    platform: str
    app_id: str
    bloks_version_id: str
    capabilities: str
    user_agent: str
    app_version: str = "410.2.0.33.71"
    device_model: str = "iPhone 15 Pro"

THREADS_DEVICES: Dict[str, ThreadsDevicePreset] = {
    "threads_ios": ThreadsDevicePreset(
        name="Threads iOS (iPhone 15 Pro)",
        platform="iOS",
        app_id="1546306509211461",
        bloks_version_id="95cbfdb413e12cf21841dcfd299719b165f658155182b7989fd661be5ea52089",
        capabilities="36r/F/8=",
        user_agent="Barcelona 410.2.0.33.71 (iPhone16,1; iOS 17_6_1; en_US; en-US; scale=3.00; 1179x2556; 850146623) AppleWebKit/420+",
        device_model="iPhone 15 Pro",
    ),
    "threads_android": ThreadsDevicePreset(
        name="Threads Android (Samsung Galaxy A34 / S24)",
        platform="Android",
        app_id="3419628305025917",
        bloks_version_id="95cbfdb413e12cf21841dcfd299719b165f658155182b7989fd661be5ea52089",
        capabilities="3brTv10=",
        user_agent="Barcelona 410.2.0.33.71 Android (34/14; 450dpi; 1080x2400; samsung; SM-A346B; a34x; mt6877; en_US; 850146623)",
        device_model="Samsung Galaxy A34 5G",
    ),
    "threads_web": ThreadsDevicePreset(
        name="Threads Web Public GraphQL",
        platform="Web",
        app_id="238260118697367",
        bloks_version_id="95cbfdb413e12cf21841dcfd299719b165f658155182b7989fd661be5ea52089",
        capabilities="36r/F/8=",
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        device_model="Desktop Web",
    ),
}

def get_threads_device(preset_key: str = "threads_ios") -> ThreadsDevicePreset:
    key = preset_key.lower().replace("-", "_")
    if "android" in key or "pixel" in key or "samsung" in key or "galaxy" in key:
        return THREADS_DEVICES["threads_android"]
    if "web" in key:
        return THREADS_DEVICES["threads_web"]
    return THREADS_DEVICES["threads_ios"]
