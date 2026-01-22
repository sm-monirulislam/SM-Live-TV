import requests
import os
from datetime import datetime

# ===============================
# CONFIG
# ===============================
API_URL = os.environ.get("TOFFEE_API_URL")
OUTPUT_FILE = "Toffee.m3u"

# ===============================
# MAIN FUNCTION
# ===============================
def generate_playlist():
    print("🚀 Fetching Toffee channel list...")

    if not API_URL:
        print("❌ TOFFEE_API_URL secret not set")
        return False

    try:
        r = requests.get(API_URL, timeout=30)
        r.raise_for_status()
        data = r.json()

        # ✅ CORRECT KEY
        channels = data.get("response", [])

        if not isinstance(channels, list):
            print("❌ Invalid JSON structure (response is not list)")
            return False

        print(f"✅ Total channels: {len(channels)}")

    except Exception as e:
        print("❌ Failed to fetch JSON:", e)
        return False

    m3u = ["#EXTM3U", ""]

    for ch in channels:
        # 🔒 SAFETY CHECK
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

        # EXTINF
        m3u.append(
            f'#EXTINF:-1 group-title="{group}" tvg-logo="{logo}",{name}'
        )

        # USER AGENT
        if ua:
            m3u.append(f"#EXTVLCOPT:http-user-agent={ua}")

        # COOKIE
        if cookie:
            m3u.append(f'#EXTHTTP:{{"cookie":"{cookie}"}}')

        # STREAM LINK
        m3u.append(link)
        m3u.append("")

    # ===============================
    # WRITE FILE
    # ===============================
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(m3u))

    print(f"✅ Playlist generated: {OUTPUT_FILE}")
    print("🕓 Updated:", datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"))
    return True


# ===============================
# ENTRY POINT
# ===============================
if __name__ == "__main__":
    if not generate_playlist():
        exit(1)
