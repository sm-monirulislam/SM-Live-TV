import requests
import os
from datetime import datetime

# ✅ API URL from GitHub Secret
API_URL = os.environ.get("AYNAOTT_API_URL")

def generate_playlist():
    print("🚀 Starting Auto Playlist Generator...")

    if not API_URL:
        print("❌ AYNAOTT_API_URL secret not found")
        return True  # skip, fail না

    print("📡 Fetching data from API...")

    try:
        response = requests.get(API_URL, timeout=20)
        response.raise_for_status()
        api_data = response.json()
    except Exception as e:
        print(f"❌ API Fetch Error: {e}")
        return True

    print("🔍 RAW API RESPONSE:", api_data)

    # ✅ NEW FORMAT HANDLE
    if not isinstance(api_data, dict):
        print("⚠️ Invalid API root format")
        return True

    channels = api_data.get("response")

    if not isinstance(channels, list) or len(channels) == 0:
        print("⚠️ No channels found, skipping update")
        return True

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
                url = ch.get("url", "").strip()
                group = ch.get("category", "Ayna")

                if not url:
                    continue

                f.write(
                    f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n'
                )
                f.write(f"{url}\n\n")

                channel_count += 1

            # ✅ footer info
            f.write(
                f"# Updated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            )
            f.write(f"# Channels: {channel_count}\n")
            f.write(f"# Owner: {api_data.get('owner','')}\n")

        print(f"✅ Playlist generated successfully with {channel_count} channels.")
        return True

    except Exception as e:
        print(f"❌ Error writing playlist file: {e}")
        return True


if __name__ == "__main__":
    print("=========================================")
    print("🎯 AynaOTT Auto Update M3U Playlist Script")
    print("=========================================")

    generate_playlist()

    print("=========================================")
    print("✅ Process completed successfully!")
