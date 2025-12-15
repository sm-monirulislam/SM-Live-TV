import requests
import json
from datetime import datetime

# ✅ Toffee JSON API
API_URL = "https://raw.githubusercontent.com/sm-monirulislam/Toffee-Auto-Update-Playlist/refs/heads/main/toffee_tv.json"

# ✅ Output M3U file
OUTPUT_FILE = "Toffee.m3u"

def generate_playlist():
    print("🚀 Fetching Toffee channel list...")

    try:
        response = requests.get(API_URL, timeout=20)
        response.raise_for_status()
        channels = response.json()
        print(f"✅ Total channels: {len(channels)}")
    except Exception as e:
        print("❌ Failed to fetch JSON:", e)
        return

    m3u_lines = ["#EXTM3U"]

    for ch in channels:
        try:
            name = ch.get("name", "Toffee Channel")
            group = ch.get("group", "Toffee")
            logo = ch.get("logo", "")
            link = ch.get("link", "")
            user_agent = ch.get("user_agent", "")
            cookie = ch.get("cookie", "")

            if not link:
                continue

            # 🔹 Channel info
            m3u_lines.append(
                f'#EXTINF:-1 group-title="{group}" tvg-logo="{logo}",{name}'
            )

            # 🔹 Headers
            if user_agent:
                m3u_lines.append(f"#EXTVLCOPT:http-user-agent={user_agent}")
            if cookie:
                m3u_lines.append(f"#EXTVLCOPT:http-cookie={cookie}")

            # 🔹 Stream URL
            m3u_lines.append(link)

        except Exception as e:
            print("⚠️ Error processing channel:", e)

    # ✅ Save playlist
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(m3u_lines))

    print(f"✅ Playlist generated successfully: {OUTPUT_FILE}")
    print("🕓 Updated at:", datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"))

if __name__ == "__main__":
    generate_playlist()
