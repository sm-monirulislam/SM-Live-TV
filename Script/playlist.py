import requests
import json
from datetime import datetime

API_URL = "https://raw.githubusercontent.com/sm-monirulislam/Upcoming-and-Live-Sports-Data/refs/heads/main/Sports_data.json"

OUTPUT_FILE = "live_playlist.m3u"

# =========================================
# Fetch API Data
# =========================================
response = requests.get(API_URL)
data = response.json()

# =========================================
# Playlist Header
# =========================================
m3u = "#EXTM3U\n\n"

live_count = 0

# =========================================
# Only LIVE Matches
# =========================================
for match in data.get("matches", []):

    if match.get("status") != "LIVE":
        continue

    event_name = match.get("event_name", "Unknown Event")

    event_info = match.get("eventInfo", {})

    logo = event_info.get("teamAFlag", "")

    for stream in match.get("streams", []):

        channel_name = stream.get("Channel_Name", "Unknown Server")
        stream_url = stream.get("stream_url", "")
        drm_key = stream.get("drm_key", "")

        if not stream_url:
            continue

        # Header split
        if "|" in stream_url:
            url, headers = stream_url.split("|", 1)
        else:
            url = stream_url
            headers = ""

        # Playlist Entry
        m3u += (
            f'#EXTINF:-1 tvg-id="{channel_name}" '
            f'tvg-name="{event_name} - {channel_name}" '
            f'tvg-logo="{logo}" '
            f'group-title="LIVE SPORTS",{event_name} | {channel_name}\n'
        )

        # DRM info
        if drm_key:
            m3u += f'#KODIPROP:inputstream.adaptive.license_key={drm_key}\n'

        # Headers
        if headers:
            m3u += f'#EXTVLCOPT:http-user-agent={headers.replace("User-Agent=", "")}\n'

        m3u += f"{url}\n\n"

        live_count += 1

# =========================================
# Save Playlist
# =========================================
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(m3u)

print("=================================")
print("LIVE Playlist Generated")
print("=================================")
print(f"Total Live Streams : {live_count}")
print(f"Saved File         : {OUTPUT_FILE}")
print("=================================")
