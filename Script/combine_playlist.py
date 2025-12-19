import os
import json
import asyncio
import aiohttp
import re
from datetime import datetime, timedelta
from io import StringIO

# -------------------------
# FILE CONFIG
# -------------------------

m3u_files = [
    "Jagobd.m3u",
    "AynaOTT.m3u",
    "SM All TV.m3u",
    "Toffee.m3u",
    "Fancode.m3u",
    "jadoo.m3u",
    "Sports.m3u",
    "KALKATA.m3u",
    "RoarZone.m3u"
]

json_file = "Bangla Channel.json"

output_live = "Combined_Live_TV.m3u"
output_dead = "offline.m3u"

EPG_URL = "https://raw.githubusercontent.com/sm-monirulislam/SM-Live-TV/refs/heads/main/epg.xml"

EXTINF_PREFIX = "#EXTINF:"
re_group_title = re.compile(r'group-title="(.*?)"')

# ❌ যেগুলোর লিংক চেক হবে না
skip_check_groups = ["RoarZone", "Fancode", "Sports", "Toffee", "AynaOTT"]

# ========================================================
# BETTER SMART CHECKER (ONLY CHANGE)
# ========================================================

async def smart_check(session, url):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "*/*",
        "Connection": "keep-alive"
    }

    # 1️⃣ Primary GET check (best for IPTV)
    try:
        async with session.get(
            url,
            timeout=aiohttp.ClientTimeout(total=7),
            headers=headers,
            allow_redirects=True
        ) as r:
            if r.status == 200:
                chunk = await r.content.read(2048)
                if chunk:
                    return True
    except:
        pass

    # 2️⃣ Fallback HEAD check
    try:
        async with session.head(
            url,
            timeout=aiohttp.ClientTimeout(total=4),
            headers=headers,
            allow_redirects=True
        ) as r:
            if r.status == 200:
                return True
    except:
        pass

    return False

# ========================================================
# MAIN
# ========================================================

async def main():
    live_buf = StringIO()
    dead_buf = StringIO()

    all_entries = []
    total_found = 0

    # -------------------------------
    # STEP 1: M3U COMBINE
    # -------------------------------
    for file_name in m3u_files:
        if not os.path.exists(file_name):
            continue

        group_name = os.path.splitext(os.path.basename(file_name))[0]

        with open(file_name, "r", encoding="utf-8", errors="replace") as f:
            lines = [l.strip() for l in f if l.strip()]

        i = 0
        while i < len(lines):
            if lines[i].startswith(EXTINF_PREFIX):
                line = lines[i]

                if 'group-title="' in line:
                    line = re_group_title.sub(
                        f'group-title="{group_name}"', line
                    )
                else:
                    line = re.sub(
                        r'#EXTINF:-1(.*?),',
                        rf'#EXTINF:-1\1 group-title="{group_name}",',
                        line
                    )

                block = [line]
                i += 1
                while i < len(lines) and not lines[i].startswith(EXTINF_PREFIX):
                    block.append(lines[i])
                    i += 1

                url = block[-1]
                all_entries.append((block, url))
                total_found += 1
            else:
                i += 1

    # -------------------------------
    # STEP 2: JSON ADD
    # -------------------------------
    if os.path.exists(json_file):
        with open(json_file, "r", encoding="utf-8") as jf:
            json_data = json.load(jf)

        group_name = os.path.splitext(json_file)[0]

        for name, info in json_data.items():
            links = info.get("links", [])
            if not links:
                continue

            url = links[0].get("url", "")
            if not url:
                continue

            extinf = (
                f'#EXTINF:-1 tvg-logo="{info.get("tvg_logo","")}" '
                f'group-title="{group_name}",{name}'
            )
            all_entries.append(([extinf, url], url))
            total_found += 1

    # -------------------------------
    # STEP 3: CHECK
    # -------------------------------
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(
            *[smart_check(session, url) for _, url in all_entries]
        )

    alive, dead = [], []

    for idx, status in enumerate(results):
        block, _ = all_entries[idx]
        m = re_group_title.search(block[0])
        grp = m.group(1) if m else ""

        if grp in skip_check_groups or status:
            alive.append(block)
        else:
            dead.append(block)

    # -------------------------------
    # HEADER (TOP OF PLAYLIST)
    # -------------------------------
    bd_time = datetime.utcnow() + timedelta(hours=6)
    header = (
        "#=================================\n"
        "# 🖥️ Developed by: Monirul Islam\n"
        "# 🔗 Telegram: https://t.me/monirul_Islam_SM\n"
        f"# 🕒 Last Updated: {bd_time.strftime('%Y-%m-%d %H:%M:%S')} (BD Time)\n"
        f"# 📺 Channels Count: {len(alive)}\n"
        "# 🔒 Usage: Personal / Educational\n"
        "#=================================\n\n"
    )

    live_buf.write(header)
    live_buf.write(f'#EXTM3U url-tvg="{EPG_URL}"\n\n')

    dead_buf.write(header)
    dead_buf.write(f'#EXTM3U url-tvg="{EPG_URL}"\n\n')

    # -------------------------------
    # WRITE FILES
    # -------------------------------
    for block in alive:
        live_buf.write("\n".join(block) + "\n\n")

    for block in dead:
        dead_buf.write("\n".join(block) + "\n\n")

    with open(output_live, "w", encoding="utf-8") as f:
        f.write(live_buf.getvalue())

    with open(output_dead, "w", encoding="utf-8") as f:
        f.write(dead_buf.getvalue())

    print("DONE")
    print("Total:", total_found)
    print("Live :", len(alive))
    print("Dead :", len(dead))


asyncio.run(main())
