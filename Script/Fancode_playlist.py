import requests
import json
import os
from datetime import datetime

# ✅ তোমার API URL
API_URL = "https://raw.githubusercontent.com/IPTVFlixBD/Fancode-BD/refs/heads/main/data.json"

def generate_playlist():
    print("🚀 Starting Auto Playlist Generator...")
    print("📡 Fetching data from API...")

    try:
        response = requests.get(API_URL, timeout=20)
        response.raise_for_status()
        try:
            data = response.json()
        except json.JSONDecodeError:
            data = json.loads(response.text.strip())
    except Exception as e:
        print(f"❌ API Fetch Error: {e}")
        return False

    # ✅ তোমার JSON structure অনুযায়ী matches লিস্ট বের করো
    matches = data.get("matches", [])
    if not matches:
        print("⚠️ No matches found in API response.")
        return False

    file_path = "Fancode.m3u"  # 🎯 ফাইলের নাম পরিবর্তন করা হলো

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            # Always write M3U header
            f.write("#EXTM3U\n")

            live_count = 0
            for match in matches:
                if not isinstance(match, dict):
                    continue

                # শুধুমাত্র LIVE ম্যাচগুলো playlist-এ নাও
                if str(match.get("status", "")).upper() != "LIVE":
                    continue

                name = match.get("title", "Unknown Match")
                logo = match.get("src", "")
                group = match.get("event_category", "Sports")
                url = match.get("adfree_url") or match.get("dai_url")

                if not url:
                    continue  # কোনো লিংক না থাকলে স্কিপ করো

                f.write(f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n')
                f.write(f"{url}\n")
                live_count += 1

            f.write(f"# Updated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        if live_count == 0:
            print("⚠️ No LIVE matches found — playlist empty.")
        else:
            print(f"✅ Playlist generated successfully with {live_count} LIVE matches.")

        return True

    except Exception as e:
        print(f"❌ Error writing playlist file: {e}")
        return False


if __name__ == "__main__":
    print("=========================================")
    print("🎯 Fancode Auto Update M3U Playlist Script")
    print("=========================================")
    success = generate_playlist()
    print("=========================================")
    if not success:
        print("❌ Process failed.")
        exit(1)
    else:
        print("✅ Process completed successfully!")
