import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load secrets from .env
load_dotenv()

# ✅ API URL from Secret
API_URL = os.getenv("CRICHD_API_URL")

# ✅ Output M3U File
OUTPUT_FILE = "Sports.m3u"

def generate_playlist():
    print("🚀 Fetching CricHD JSON data...")

    if not API_URL:
        print("❌ ERROR: API Secret (CRICHD_API_URL) not found!")
        return

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
                continue  # skip empty link

            # Build entry
            m3u_lines.append(f'#EXTINF:-1 tvg-logo="{logo}",{name}')
            if referer:
                m3u_lines.append(f"#EXTVLCOPT:http-referrer={referer}")
            if origin:
                m3u_lines.append(f"#EXTVLCOPT:http-origin={origin}")
            m3u_lines.append(link)

        except Exception as e:
            print(f"⚠️ Error processing channel: {e}")

    # Save to file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(m3u_lines))

    print(f"✅ Playlist generated: {OUTPUT_FILE}")
    print("🕓 Updated at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == "__main__":
    generate_playlist()
