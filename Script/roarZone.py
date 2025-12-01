import requests

JSON_URL = "https://raw.githubusercontent.com/sm-monirulislam/RoarZone-Auto-Update-playlist/refs/heads/main/RoarZone.json"
OUTPUT = "RoarZone.m3u"

def main():
    print("Downloading JSON...")
    response = requests.get(JSON_URL)
    data = response.json()

    m3u_lines = ["#EXTM3U"]

    for item in data:
        title = item.get("title", "Unknown")
        logo = item.get("logo", "")
        category = item.get("category", "Others")
        url = item.get("stream_url", "")

        extinf = f'#EXTINF:-1 tvg-logo="{logo}" group-title="{category}",{title}'
        m3u_lines.append(extinf)
        m3u_lines.append(url)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(m3u_lines))

    print("Generated:", OUTPUT)


if __name__ == "__main__":
    main()
