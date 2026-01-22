import requests
import os
from datetime import datetime

# ✅ Toffee JSON API from GitHub Secret
API_URL = os.environ.get("TOFFEE_API_URL")

# ✅ Output file
OUTPUT_FILE = "Toffee.m3u"

def generate_playlist():
    print("🚀 Fetching Toffee channel list...")

    if not API_URL:
        print("⚠️ TOFFEE_API_URL secret not set (script will stop).")
        return False

    try:
        r = requests.get(API_URL, timeout=20)
        r.raise_for_status()
        data = r.json()

        channels = data.get("response", [])
        print(f"✅ Total channels: {len(channels)}")

    except Exception as e:
        print("❌ Failed to fetch JSON:", e)
        return False

    m3u = ["#EXTM3U", ""]

    for ch in channels:
        if not isinstance(ch, dict):
            continue

        link = ch.get("link")
        if not link:
            continue

        name = ch.get("name", "Toffee Channel")
        group = ch.get("category_name", "Toffee")
        logo = ch.get("logo", "")

        headers = ch.get("headers", {})
        ua = headers.get("user-agent", "")
        cookie = headers.get("cookie", "")

        m3u.append(
            f'#EXTINF:-1 group-title="{group}" tvg-logo="{logo}",{name}'
        )

        if ua:
            m3u.append(f"#EXTVLCOPT:http-user-agent={ua}")

        if cookie:
            m3u.append(f'#EXTHTTP:{{"cookie":"{cookie}"}}')

        m3u.append(link)
        m3u.append("")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(m3u))

    print(f"✅ Playlist generated: {OUTPUT_FILE}")
    print("🕓 Updated:", datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"))
    return True


if __name__ == "__main__":
    if not generate_playlist():
        exit(1)
