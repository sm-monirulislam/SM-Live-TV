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

# ✅ EPG URL (ONLY ADDITION)
EPG_URL = "https://raw.githubusercontent.com/sm-monirulislam/SM-Live-TV/refs/heads/main/epg.xml"

EXTINF_PREFIX = "#EXTINF:"
re_group_title = re.compile(r'group-title="(.*?)"')

# ❌ যেগুলোর লিংক চেক হবে না (UPDATED)
skip_check_groups = ["RoarZone", "Fancode", "Sports", "Toffee", "AynaOTT"]


# ========================================================
# SMART LIVE CHECK (UNCHANGED)
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
# MAIN
# ========================================================
async def main():
    live_buf = StringIO()
    dead_buf = StringIO()

    # ✅ EPG added in header
    live_buf.write(f'#EXTM3U url-tvg="{EPG_URL}"\n\n')
    dead_buf.write(f'#EXTM3U url-tvg="{EPG_URL}"\n\n')

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
        n = len(lines)

        while i < n:
            line = lines[i]

            if line.startswith(EXTINF_PREFIX):

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
                j = i + 1

                while j < n and not lines[j].startswith(EXTINF_PREFIX):
                    block.append(lines[j])
                    j += 1

                url = block[-1]
                all_entries.append((block, url))
                total_found += 1
                i = j
            else:
                i += 1

    # -------------------------------
    # STEP 2: JSON ADD
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
            block = [extinf, url]
            all_entries.append((block, url))
            total_found += 1

    # -------------------------------
    # STEP 3: SMART CHECK
    # -------------------------------
    async with aiohttp.ClientSession() as session:
        tasks = [smart_check(session, url) for _, url in all_entries]
        results = await asyncio.gather(*tasks)

    alive_list = []
    dead_list = []

    for i, status in enumerate(results):
        block, url = all_entries[i]

        grp = ""
        if 'group-title="' in block[0]:
            m = re_group_title.search(block[0])
            if m:
                grp = m.group(1)

        if grp in skip_check_groups:
            alive_list.append(block)
            print(f"⏭ SKIPPED (Auto-LIVE): {grp}")
        elif status:
            alive_list.append(block)
            print(f"✔ LIVE: {url}")
        else:
            dead_list.append(block)
            print(f"✘ DEAD: {url}")

    # -------------------------------
    # STEP 4: WRITE FILES
    # -------------------------------
    for block in alive_list:
        for line in block:
            live_buf.write(line + "\n")
        live_buf.write("\n")

    for block in dead_list:
        for line in block:
            dead_buf.write(line + "\n")
        dead_buf.write("\n")

    bd_time = datetime.utcnow() + timedelta(hours=6)
    stamp = f"# Last Updated: {bd_time.strftime('%Y-%m-%d %H:%M:%S')} BD Time\n"

    live_buf.write(stamp)
    dead_buf.write(stamp)

    with open(output_live, "w", encoding="utf-8") as f:
        f.write(live_buf.getvalue())

    with open(output_dead, "w", encoding="utf-8") as f:
        f.write(dead_buf.getvalue())

    print("\n✅ DONE")
    print(f"Total Found : {total_found}")
    print(f"Live        : {len(alive_list)}")
    print(f"Dead        : {len(dead_list)}")


asyncio.run(main())
