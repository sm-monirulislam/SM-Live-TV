import requests

API_URL = "https://raw.githubusercontent.com/sm-monirulislam/Upcoming-and-Live-Sports-Data/refs/heads/main/Sports_data.json"

OUTPUT_FILE = "live_playlist.m3u"

# =========================================
# Fetch API
# =========================================
response = requests.get(API_URL)
data = response.json()

# =========================================
# Playlist Header
# =========================================
m3u = "#EXTM3U\n\n"

total_streams = 0

# =========================================
# Generate Playlist
# =========================================
for match in data.get("matches", []):

    # Only LIVE matches
    if match.get("status") != "LIVE":
        continue

    event_name = match.get("event_name", "Unknown Event")

    event_info = match.get("eventInfo", {})

    # Same logo for all servers
    logo = event_info.get("teamAFlag", "")

    streams = match.get("streams", [])

    for stream in streams:

        channel_name = stream.get("Channel_Name", "Server")

        drm_key = stream.get("drm_key", "")

        stream_url = stream.get("stream_url", "").strip()

        if not stream_url:
            continue

        # Remove headers after |
        if "|" in stream_url:
            stream_url = stream_url.split("|")[0]

        # =========================================
        # Playlist Format
        # =========================================
        m3u += (
            f'#EXTINF:-1 '
            f'tvg-logo="{logo}" '
            f'group-title="LIVE SPORTS",'
            f'{event_name} | {channel_name} [DRM]\n'
        )

        # DRM Type
        m3u += '#KODIPROP:inputstream.adaptive.license_type=clearkey\n'

        # DRM Key
        if drm_key:
            m3u += f'#KODIPROP:inputstream.adaptive.license_key={drm_key}\n'

        # Stream URL
        m3u += f'{stream_url}\n\n'

        total_streams += 1

# =========================================
# Save Playlist
# =========================================
with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    file.write(m3u)

print("=================================")
print("LIVE DRM Playlist Generated")
print("=================================")
print(f"Total Streams : {total_streams}")
print(f"Saved File    : {OUTPUT_FILE}")
print("=================================")
