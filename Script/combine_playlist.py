import os
import json
import asyncio
import aiohttp
import re
from datetime import datetime, timedelta
from io import StringIO

# -------------------------
# FILE LIST CONFIG
# -------------------------
m3u_files = [
    "Jagobd.m3u",
    "AynaOTT.m3u",
    "SM All TV.m3u",
    "Toffee.m3u",
    "Fancode.m3u",
    "jadoo.m3u",
    "Sports.m3u",
    "KALKATA.m3u"
]

json_file = "Bangla Channel.json"
output_live = "Combined_Live_TV.m3u"
output_dead = "offline.m3u"

EXTINF_PREFIX = "#EXTINF:"
re_group_title = re.compile(r'group-title="(.*?)"')


# ========================================================
# 🔥 SMART Stream Checker (HEAD → Retry → GET Chunk)
# ========================================================
async def smart_check(session, url):
    # Step 1: HEAD
    try:
        async with session.head(url, timeout=4) as r:
            if r.status == 200:
                return True
    except:
        pass

    # Step 2: Retry
    await asyncio.sleep(0.2)
    try:
        async with session.head(url, timeout=4) as r:
            if r.status == 200:
                return True
    except:
        pass

    # Step 3: Small GET
    try:
        async with session.get(url, timeout=6) as r:
            chunk = await r.content.read(1024)
            if r.status == 200 and len(chunk) > 0:
                return True
    except:
        pass

    return False


# ========================================================
# 🔥 Main Combine + Check Logic
# ========================================================
async def main():
    live_buf = StringIO()
    dead_buf = StringIO()

    live_buf.write("#EXTM3U\n\n")
    dead_buf.write("#EXTM3U\n\n")

    all_entries = []  # store (extinf, url)
    total_found = 0

    # -------------------------------
    # Step 1: Combine all M3U files
    # -------------------------------
    for file_name in m3u_files:
        if not os.path.exists(file_name):
            continue

        group_name = os.path.splitext(os.path.basename(file_name))[0]

        with open(file_name, "r", encoding="utf-8", errors="replace") as f:
            lines = [l.strip() for l in f if l.strip()]

        i = 0
        n = len(lines)

        while i < n:
            line = lines[i]

            if line.startswith(EXTINF_PREFIX):
                # Replace or add group-title
                if 'group-title="' in line:
                    line = re_group_title.sub(f'group-title="{group_name}"', line)
                else:
                    parts = line.split(",", 1)
                    if len(parts) == 2:
                        line = f'{parts[0]} group-title="{group_name}",{parts[1]}'

                segment = [line]
                j = i + 1
                while j < n and not lines[j].startswith(EXTINF_PREFIX):
                    segment.append(lines[j])
                    j += 1

                url = segment[-1]
                all_entries.append((segment[0], url))
                total_found += 1
                i = j
            else:
                i += 1

    # -------------------------------
    # Step 2: Add JSON channels
    # -------------------------------
    if os.path.exists(json_file):
        with open(json_file, "r", encoding="utf-8") as jf:
            json_data = json.load(jf)

        group_name = os.path.splitext(os.path.basename(json_file))[0]

        for name, info in json_data.items():
            url = ""
            if "links" in info and info["links"]:
                url = info["links"][0].get("url", "")

            if not url:
                continue

            extinf = (
                f'#EXTINF:-1 tvg-logo="{info.get("tvg_logo","")}" '
                f'group-title="{group_name}",{name}'
            )
            all_entries.append((extinf, url))
            total_found += 1

    print(f"\n🔍 Total streams found: {total_found}\n")

    # -------------------------------
    # Step 3: Smart Check All URLs
    # -------------------------------
    alive_list = []
    dead_list = []

    async with aiohttp.ClientSession() as session:
        tasks = [smart_check(session, url) for _, url in all_entries]
        results = await asyncio.gather(*tasks)

    for i, status in enumerate(results):
        extinf, url = all_entries[i]

        if status:
            alive_list.append((extinf, url))
            print(f"✔ LIVE: {url}")
        else:
            dead_list.append((extinf, url))
            print(f"✘ DEAD: {url}")

    # -------------------------------
    # Step 4: Write LIVE playlist
    # -------------------------------
    for ext, url in alive_list:
        live_buf.write(f"{ext}\n{url}\n\n")

    # -------------------------------
    # Step 5: Write DEAD playlist
    # -------------------------------
    for ext, url in dead_list:
        dead_buf.write(f"{ext}\n{url}\n\n")

    # Timestamp
    bd_time = datetime.utcnow() + timedelta(hours=6)
    stamp = f"# Last Updated: {bd_time.strftime('%Y-%m-%d %H:%M:%S')} BD Time\n"

    live_buf.write(stamp)
    dead_buf.write(stamp)

    # Save files
    with open(output_live, "w", encoding="utf-8") as lf:
        lf.write(live_buf.getvalue())

    with open(output_dead, "w", encoding="utf-8") as df:
        df.write(dead_buf.getvalue())

    # Summary
    print("\n=====================================")
    print("    ✅ Playlist Build Completed")
    print("=====================================")
    print(f"Total Found : {total_found}")
    print(f"Alive       : {len(alive_list)}")
    print(f"Dead        : {len(dead_list)}")
    print(f"Output Live : {output_live}")
    print(f"Output Dead : {output_dead}")
    print("=====================================\n")


# Run async
asyncio.run(main())
