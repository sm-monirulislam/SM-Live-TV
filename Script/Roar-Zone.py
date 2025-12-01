import requests
import json
import os
from datetime import datetime

# ✅ নতুন API URL
API_URL = "https://raw.githubusercontent.com/sm-monirulislam/RoarZone-Auto-Update-playlist/refs/heads/main/RoarZone.json"

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

    # ⬇️ তোমার API সরাসরি list আকারে আসে
    if not isinstance(data, list) or len(data) == 0:
        print("⚠️ Invalid API response or empty list.")
        return False

    file_path = "RoarZone.m3u"

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")

            channel_count = 0

            for item in data:
                if not isinstance(item, dict):
                    continue

                name = item.get("title", "Unknown")
                logo = item.get("logo", "")
                group = item.get("category", "Others")
                url = item.get("stream_url")

                if not url:
                    continue  # stream url না থাকলে skip

                f.write(f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n')
                f.write(f"{url}\n")

                channel_count += 1

            f.write(f"# Updated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        if channel_count == 0:
            print("⚠️ No channels found — playlist empty.")
        else:
            print(f"✅ Playlist generated successfully with {channel_count} channels.")

        return True

    except Exception as e:
        print(f"❌ Error writing playlist file: {e}")
        return False


if __name__ == "__main__":
    print("=========================================")
    print("🎯 RoarZone Auto Update M3U Playlist Script")
    print("=========================================")
    success = generate_playlist()
    print("=========================================")
    if not success:
        print("❌ Process failed.")
        exit(1)
    else:
        print("✅ Process completed successfully!")
