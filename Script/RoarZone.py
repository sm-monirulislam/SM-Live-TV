import requests
import os

# ================== CONFIG ==================
API_URL = os.getenv("API_URL")  # 🔐 Secret থেকে আসবে
OUTPUT_FILE = "RoarZone.m3u"

# ================== FETCH JSON ==================
def fetch_json(url):
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print("Error fetching JSON:", e)
        return None

# ================== CREATE M3U ==================
def create_m3u(json_data):
    lines = ["#EXTM3U"]

    channels = json_data.get("response", [])

    for item in channels:
        name = item.get("name", "No Name")
        stream = item.get("url", "")
        logo = item.get("logo", "")
        group = item.get("group", "Live TV")

        if stream:
            lines.append(
                f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}'
            )
            lines.append(stream)

    return "\n".join(lines)

# ================== MAIN ==================
def main():
    if not API_URL:
        print("❌ API_URL not set!")
        return

    data = fetch_json(API_URL)

    if not data:
        print("❌ No data found!")
        return

    m3u_content = create_m3u(data)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(m3u_content)

    print(f"✅ Playlist created: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
