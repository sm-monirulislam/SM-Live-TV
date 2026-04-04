import requests
import os
from datetime import datetime

# API URL from GitHub Secret
API_URL = os.environ.get("CRICHD_API_URL")

OUTPUT_FILE = "Sports.m3u"

def generate_playlist():
    if not API_URL:
        print("❌ CRICHD_API_URL secret not found")
        return

    print("🚀 Fetching CricHD JSON data...")
    try:
        response = requests.get(API_URL, timeout=20)
        response.raise_for_status()
        json_data = response.json()

        # Extract channel list
        data = json_data.get("response", [])

        print(f"✅ JSON data fetched! Total channels: {len(data)}")

    except Exception as e:
        print("❌ Error fetching JSON:", e)
        return

    m3u_lines = ["#EXTM3U"]

    for ch in data:
        name = ch.get("title", "Unknown Channel")
        logo = ch.get("logo", "")
        link = ch.get("url", "")

        # 🔥 FIX: handle both referer & Referer
        referer = ch.get("referer") or ch.get("Referer", "")

        category = ch.get("category", "Sports")

        if not link:
            continue

        m3u_lines.append(
            f'#EXTINF:-1 tvg-logo="{logo}" group-title="{category}",{name}'
        )

        if referer:
            m3u_lines.append(f"#EXTVLCOPT:http-referrer={referer}")

        m3u_lines.append(link)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(m3u_lines))

    print(f"✅ Playlist generated: {OUTPUT_FILE}")
    print("🕓 Updated at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == "__main__":
    generate_playlist()
