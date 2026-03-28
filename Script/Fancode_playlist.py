import requests
import os

# GitHub Secret থেকে API নিবে
API_URL = os.getenv("FANCODE_API")

OUTPUT_FILE = "Fancode.m3u"

def generate_playlist():
    if not API_URL:
        print("❌ FANCODE_API secret not found!")
        return

    print("🚀 Fetching API data...")

    try:
        response = requests.get(API_URL, timeout=20)
        data = response.json()
    except Exception as e:
        print("❌ Error fetching API:", e)
        return

    matches = data.get("matches", [])

    playlist = "#EXTM3U\n"

    for match in matches:
        title = match.get("title", "No Title")
        logo = match.get("src", "")
        group = match.get("event_category", "Fancode")
        status = match.get("status", "")
        url = match.get("adfree_url", "")

        # stream না থাকলে skip
        if not url:
            continue

        name = f"{title} [{status}]"

        playlist += f'#EXTINF:-1 tvg-name="{name}" tvg-logo="{logo}" group-title="{group}",{name}\n'
        playlist += f"{url}\n"

    # file save
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(playlist)

    print(f"✅ Playlist saved as {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_playlist()
