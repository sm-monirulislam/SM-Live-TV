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

EXTINF_PREFIX = "#EXTINF:"
re_group_title = re.compile(r'group-title="(.*?)"')

# -------------------------
# ⛔ এই গ্রুপগুলোর লিংক চেক হবে না
# -------------------------
skip_check_groups = ["RoarZone", "Fancode"]


# ========================================================
# 🔥 Smart Live Checker Function
# ========================================================
async def smart_check(session, url):
    try:
        async with session.head(url, timeout=4) as r:
            if r.status == 200:
                return True
    except:
        pass

    await asyncio.sleep(0.2)
    try:
        async with session.head(url, timeout=4) as r:
            if r.status == 200:
                return True
    except:
        pass

    try:
        async with session.get(url, timeout=6) as r:
            chunk = await r.content.read(1024)
            if r.status == 200 and len(chunk) > 0:
                return True
    except:
        pass

    return False


# ========================================================
# 🔥 MAIN FUNCTION
# ========================================================
async def main():
    live_buf = StringIO()
    dead_buf = StringIO()

    live_buf.write("#EXTM3U\n\n")
    dead_buf.write("#EXTM3U\n\n")

    all_entries = []
    total_found = 0

    # -------------------------------
    # Step 1: M3U Combine
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
    # Step 2: JSON Add
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

    # ⚠️ Step 3 removed fully — offline.m3u old links WON’T be reloaded

    # -------------------------------
    # Step 4: Smart Check All URLs
    # -------------------------------
    alive_list = []
    dead_list = []

    async with aiohttp.ClientSession() as session:
        tasks = [smart_check(session, url) for _, url in all_entries]
        results = await asyncio.gather(*tasks)

    for i, status in enumerate(results):
        extinf, url = all_entries[i]

        # Skip checking selected groups
        grp = ""
        m = re_group_title.search(extinf)
        if m:
            grp = m.group(1)

        if grp in skip_check_groups:
            alive_list.append((extinf, url))
            print(f"⏭ SKIPPED (Auto-LIVE): {grp} → {url}")
            continue

        if status:
            alive_list.append((extinf, url))
            print(f"✔ LIVE: {url}")
        else:
            dead_list.append((extinf, url))
            print(f"✘ DEAD: {url}")

    # -------------------------------
    # Step 5: Write LIVE + DEAD files
    # -------------------------------
    for ext, url in alive_list:
        live_buf.write(f"{ext}\n{url}\n\n")

    for ext, url in dead_list:
        dead_buf.write(f"{ext}\n{url}\n\n")

    bd_time = datetime.utcnow() + timedelta(hours=6)
    stamp = f"# Last Updated: {bd_time.strftime('%Y-%m-%d %H:%M:%S')} BD Time\n"

    live_buf.write(stamp)
    dead_buf.write(stamp)

    with open(output_live, "w", encoding="utf-8") as lf:
        lf.write(live_buf.getvalue())

    with open(output_dead, "w", encoding="utf-8") as df:
        df.write(dead_buf.getvalue())

    print("\n=====================================")
    print("    ✅ Playlist Build Completed")
    print("=====================================")
    print(f"Total Found : {total_found}")
    print(f"Alive       : {len(alive_list)}")
    print(f"Dead        : {len(dead_list)}")
    print(f"Output Live : {output_live}")
    print(f"Output Dead : {output_dead}")
    print("=====================================\n")


asyncio.run(main())
