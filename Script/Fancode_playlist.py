import requests
from datetime import datetime

API_1 = "https://raw.githubusercontent.com/IPTVFlixBD/Fancode-BD/refs/heads/main/data.json"
API_2 = "https://raw.githubusercontent.com/jitendra-unatti/fancode/refs/heads/main/data/fancode.json"

def convert_in_to_bd(url):
    if not url:
        return None
    return url.replace(
        "https://in-mc-fdlive.fancode.com",
        "https://bd-mc-fdlive.fancode.com"
    )

def fetch_matches(api_url):
    r = requests.get(api_url, timeout=20)
    r.raise_for_status()
    return r.json().get("matches", [])

def generate_playlist():
    written_urls = set()   # 🔥 duplicate checker
    live_count = 0

    with open("Fancode.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")

        # 🔹 API 1 (NO URL change)
        for m in fetch_matches(API_1):
            if str(m.get("status", "")).upper() != "LIVE":
                continue

            url = m.get("adfree_url") or m.get("dai_url")
            if not url or url in written_urls:
                continue

            name = m.get("title", "Unknown Match")
            logo = m.get("src", "")
            group = m.get("event_category", "Sports")

            f.write(f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n')
            f.write(f"{url}\n")

            written_urls.add(url)
            live_count += 1

        # 🔹 API 2 (ONLY here in → bd replace)
        for m in fetch_matches(API_2):
            if str(m.get("status", "")).upper() != "LIVE":
                continue

            stream = m.get("STREAMING_CDN", {})
            url = (
                stream.get("Primary_Playback_URL")
                or stream.get("fancode_cdn")
                or stream.get("dai_google_cdn")
            )

            url = convert_in_to_bd(url)
            if not url or url in written_urls:
                continue

            name = m.get("title", "Unknown Match")
            logo = m.get("image", "")
            group = m.get("category", "Sports")

            f.write(f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n')
            f.write(f"{url}\n")

            written_urls.add(url)
            live_count += 1

        f.write(f"# Updated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    print(f"✅ Done! {live_count} unique LIVE matches added.")

if __name__ == "__main__":
    generate_playlist()
