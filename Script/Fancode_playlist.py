import requests
import os

API = os.getenv("API_URL")
OUTPUT = "Fancode.m3u"

playlist = "#EXTM3U\n"

r = requests.get(API)
data = r.json()

matches = data.get("matches", [])

for match in matches:
    title = match.get("title", "")
    logo = match.get("src", "")
    group = match.get("event_category", "")
    url = match.get("adfree_url", "")

    if url:
        playlist += f'#EXTINF:-1 tvg-name="{title}" tvg-logo="{logo}" group-title="{group}",{title}\n'
        playlist += f"{url}\n"

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(playlist)

print("Fancode.m3u updated")
