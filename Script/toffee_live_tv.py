import requests
import os

API_URL = os.environ.get("TOFFEE_API_URL")
OUTPUT_FILE = "Toffee.m3u"

def generate_playlist():
    # 🔒 API empty / invalid হলে কিছুই করবে না
    if not API_URL or not isinstance(API_URL, str) or not API_URL.strip():
        return

    try:
        r = requests.get(API_URL.strip(), timeout=30)
        if r.status_code != 200:
            return

        data = r.json()
        if not isinstance(data, dict):
            return

        channels = data.get("response")
        if not isinstance(channels, list) or not channels:
            return

    except Exception:
        return

    m3u = ["#EXTM3U", ""]
    valid_count = 0

    for ch in channels:
        if not isinstance(ch, dict):
            continue

        link = ch.get("link")
        if not isinstance(link, str) or not link.strip():
            continue

        name = ch.get("name") or "Toffee Channel"
        group = ch.get("category_name") or "Toffee"
        logo = ch.get("logo") or ""

        headers = ch.get("headers") if isinstance(ch.get("headers"), dict) else {}
        ua = headers.get("user-agent") or ""
        cookie = headers.get("cookie") or ""

        m3u.append(
            f'#EXTINF:-1 group-title="{group}" tvg-logo="{logo}",{name}'
        )

        if isinstance(ua, str) and ua.strip():
            m3u.append(f"#EXTVLCOPT:http-user-agent={ua}")

        if isinstance(cookie, str) and cookie.strip():
            m3u.append(f'#EXTHTTP:{{"cookie":"{cookie}"}}')

        m3u.append(link.strip())
        m3u.append("")
        valid_count += 1

    # 🔒 একটাও valid channel না থাকলে কিছুই লিখবে না
    if valid_count == 0:
        return

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(m3u))


if __name__ == "__main__":
    generate_playlist()
