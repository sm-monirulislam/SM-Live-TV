import requests
import json
import os
from datetime import datetime

# ✅ API URL from GitHub Actions Secret
API_URL = os.environ.get("CRICHD_API_URL")

# ✅ Output M3U File
OUTPUT_FILE = "Sports.m3u"

def generate_playlist():
    if not API_URL:
        print("❌ CRICHD_API_URL secret পাওয়া যায়নি")
        return

    print("🚀 Fetching CricHD JSON data from GitHub Secret...")

    try:
        response = requests.get(API_URL, timeout=20)
        response.raise_for_status()
        data = response.json()
        print(f"✅ JSON data fetched successfully! Total channels: {len(data)}")
    except Exception as e:
        print("❌ Error fetching JSON:", e)
        return

    m3u_lines = ["#EXTM3U"]

    # ✅ Iterate through JSON list
    for ch in data:
        try:
            name = ch.get("name", "Unknown Channel")
            logo = ch.get("logo", "")
            link = ch.get("link", "")
            referer = ch.get("referer", "")
            origin = ch.get("origin", "")

            if not link:
                continue

            m3u_lines.append(f'#EXTINF:-1 tvg-logo="{logo}",{name}')

            if referer:
                m3u_lines.append(f"#EXTVLCOPT:http-referrer={referer}")
            if origin:
                m3u_lines.append(f"#EXTVLCOPT:http-origin={origin}")

            m3u_lines.append(link)

        except Exception as e:
            print(f"⚠️ Error processing channel: {e}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(m3u_lines))

    print(f"✅ Playlist generated: {OUTPUT_FILE}")
    print("🕓 Updated at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    generate_playlist()
