import requests
import os
from datetime import datetime

# ================== SETTINGS ==================
API_URL = os.environ.get("ROARZONE_API_URL")
OUTPUT_FILE = "RoarZone.m3u"

def generate_playlist():
    # ❌ If API not set → silently exit
    if not API_URL:
        return True

    try:
        r = requests.get(API_URL, timeout=20)
        r.raise_for_status()
        data = r.json()
    except:
        return True   # No error print

    if not isinstance(data, dict) or "response" not in data:
        return True

    channels = data.get("response", [])
    if not isinstance(channels, list) or not channels:
        return True

    seen_urls = set()

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")

            for item in channels:
                if not isinstance(item, dict):
                    continue

                name = item.get("title", "Unknown")
                logo = item.get("logo", "")
                group = item.get("category", "Others")
                url = item.get("url")

                if not url or url in seen_urls:
                    continue

                seen_urls.add(url)

                f.write(
                    f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n'
                )
                f.write(f"{url}\n")

            f.write(
                f"# Updated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            )

        return True

    except:
        return True


if __name__ == "__main__":
    generate_playlist()
