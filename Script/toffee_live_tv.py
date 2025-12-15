import requests
from datetime import datetime

# ✅ Toffee JSON API
API_URL = "https://raw.githubusercontent.com/sm-monirulislam/Toffee-Auto-Update-Playlist/refs/heads/main/toffee_tv.json"

# ✅ Output file
OUTPUT_FILE = "Toffee.m3u"

def generate_playlist():
    print("🚀 Fetching Toffee channel list...")

    try:
        r = requests.get(API_URL, timeout=20)
        r.raise_for_status()
        channels = r.json()
        print(f"✅ Total channels: {len(channels)}")
    except Exception as e:
        print("❌ Failed to fetch JSON:", e)
        return

    m3u = ["#EXTM3U", ""]

    for ch in channels:
        link = ch.get("link")
        if not link:
            continue

        name = ch.get("name", "Toffee Channel")
        group = ch.get("group", "Toffee")
        logo = ch.get("logo", "")
        ua = ch.get("user_agent", "")
        cookie = ch.get("cookie", "")

        # EXTINF
        m3u.append(
            f'#EXTINF:-1 group-title="{group}" tvg-chno="" tvg-id="" tvg-logo="{logo}", {name}'
        )

        # User-Agent
        if ua:
            m3u.append(f"#EXTVLCOPT:http-user-agent={ua}")

        # Cookie (EXTHTTP format)
        if cookie:
            m3u.append(f'#EXTHTTP:{{"cookie":"{cookie}"}}')

        # Stream URL
        m3u.append(link)
        m3u.append("")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(m3u))

    print(f"✅ Playlist generated: {OUTPUT_FILE}")
    print("🕓 Updated:", datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"))

if __name__ == "__main__":
    generate_playlist()
