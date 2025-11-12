import requests
import json
from datetime import datetime

# ✅ API URL
API_URL = "https://raw.githubusercontent.com/hasanhabibmottakin/AynaOTT/refs/heads/main/rest_api.json"

def generate_playlist():
    print("🚀 Starting Auto Playlist Generator...")
    print("📡 Fetching data from API...")

    try:
        response = requests.get(API_URL, timeout=20)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"❌ API Fetch Error: {e}")
        return False

    channels = data.get("channels", [])
    if not channels:
        print("⚠️ No channels found in API response.")
        return False

    file_path = "AynaOTT.m3u"

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")

            channel_count = 0
            for ch in channels:
                if not isinstance(ch, dict):
                    continue

                name = ch.get("title", "Unknown Channel")
                logo = ch.get("logo", "")
                group = ch.get("category", "AynaOTT")
                url = ch.get("url", "").strip()  # ← পুরো URL সহ (যেমন token-সহ)

                if not url:
                    continue

                # ✅ প্রতিটি চ্যানেল লিখো
                f.write(f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n')
                f.write(f"{url}\n\n")

                channel_count += 1

            f.write(f"# Updated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        print(f"✅ Playlist generated successfully with {channel_count} channels.")
        return True

    except Exception as e:
        print(f"❌ Error writing playlist file: {e}")
        return False


if __name__ == "__main__":
    print("=========================================")
    print("🎯 AynaOTT Auto Update M3U Playlist Script")
    print("=========================================")
    success = generate_playlist()
    print("=========================================")
    if not success:
        print("❌ Process failed.")
        exit(1)
    else:
        print("✅ Process completed successfully!")
