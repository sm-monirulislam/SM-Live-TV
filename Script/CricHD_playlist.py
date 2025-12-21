import requests
import os
from datetime import datetime

API_URL = os.getenv("CRICHD_API_URL")
OUTPUT_FILE = "Sports.m3u"


def generate_playlist():
    print("🚀 Fetching CricHD JSON data...")

    if not API_URL:
        print("❌ ERROR: CRICHD_API_URL not found in GitHub Actions Secrets!")
        return

    try:
        response = requests.get(API_URL, timeout=20)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print("❌ Error fetching JSON:", e)
        return

    # ✅ Safe JSON handling
    if isinstance(data, dict):
        data = data.get("channels", [])

    if not isinstance(data, list):
        print("❌ Invalid JSON format")
        return

    print(f"✅ Total channels found: {len(data)}")

    m3u_lines = ["#EXTM3U"]

    for ch in data:
        try:
            name = ch.get("name", "Unknown Channel")
            logo = ch.get("logo", "")
            link = ch.get("link", "")
            referer = ch.get("referer", "")
            origin = ch.get("origin", "")

            if not link:
                continue

            m3u_lines.append(
                f'#EXTINF:-1 tvg-name="{name}" tvg-logo="{logo}",{name}'
            )

            if referer:
                m3u_lines.append(f"#EXTVLCOPT:http-referrer={referer}")

            if origin:
                m3u_lines.append(f"#EXTVLCOPT:http-origin={origin}")

            m3u_lines.append(link)

        except Exception as e:
            print("⚠️ Channel skipped:", e)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(m3u_lines))

    print(f"✅ Playlist generated: {OUTPUT_FILE}")
    print("🕒 Updated:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == "__main__":
    generate_playlist()
