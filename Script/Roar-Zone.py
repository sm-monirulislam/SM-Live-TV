import requests
import json
import os
from datetime import datetime

# GitHub Secret
API_URL = os.environ.get("ROARZONE_API_URL")
OUTPUT_FILE = "RoarZone.m3u"

def generate_playlist():
    if not API_URL:
        print("❌ ROARZONE_API_URL secret not found")
        return False

    try:
        r = requests.get(API_URL, timeout=20)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        print(f"❌ API error: {e}")
        return False

    # API must be list
    if not isinstance(data, list) or not data:
        print("❌ API response is not a list or empty")
        return False

    channel_count = 0
    seen_urls = set()

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")

            for item in data:
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

                channel_count += 1

            f.write(
                f"# Updated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            )

        print(f"✅ Playlist generated: {channel_count} channels")
        return True

    except Exception as e:
        print(f"❌ File write error: {e}")
        return False


if __name__ == "__main__":
    print("🎯 RoarZone Auto M3U Generator")
    success = generate_playlist()
    if not success:
        exit(1)
