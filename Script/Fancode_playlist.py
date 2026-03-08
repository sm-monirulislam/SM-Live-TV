import requests
import os

API = os.getenv("API_URL")   # GitHub Secret থেকে API নিবে
OUTPUT = "Fancode.m3u"

def make_playlist():
    r = requests.get(API)
    data = r.json()

    playlist = "#EXTM3U\n"

    for match in data.get("matches", []):
        title = match.get("title", "FanCode Match")
        url = match.get("adfree_url", "")
        status = match.get("status", "")

        if url:
            playlist += f'#EXTINF:-1 group-title="FanCode {status}",{title}\n'
            playlist += f"{url}\n"

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(playlist)

    print("Playlist created:", OUTPUT)

if __name__ == "__main__":
    make_playlist()
