import requests
import os

API_URL = os.getenv("FANCODE_API")

OUTPUT_FILE = "Fancode.m3u"

def generate_playlist():
    if not API_URL:
        print("❌ FANCODE_API secret not found!")
        return

    print("🚀 Fetching API data...")

    try:
        response = requests.get(API_URL, timeout=20)
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException as e:
        print(f"❌ Request Error: {e}")
        return

    except ValueError:
        print("❌ Invalid JSON response!")
        return

    matches = data.get("matches", [])

    if not matches:
        print("❌ No matches found!")
        return

    playlist = "#EXTM3U\n\n"
    added = 0

    for match in matches:
        title = match.get("title", "No Title")
        logo = match.get("src", "")
        group = match.get("event_category", "Fancode")
        status = match.get("status", "UNKNOWN")

        # New stream field
        url = match.get("fancode_bd", "").strip()

        if not url:
            continue

        name = f"{title} [{status}]"

        playlist += (
            f'#EXTINF:-1 tvg-name="{name}" '
            f'tvg-logo="{logo}" '
            f'group-title="{group}",{name}\n'
        )

        playlist += f"{url}\n\n"
        added += 1

    if added == 0:
        print("❌ No valid streams found!")
        return

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(playlist)

    print(f"✅ Playlist saved: {OUTPUT_FILE}")
    print(f"✅ Total Streams Added: {added}")

if __name__ == "__main__":
    generate_playlist()
