import os
import json
from datetime import datetime, timedelta
import re
from io import StringIO

# 🔹 M3U ফাইল তালিকা
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

# 🔹 JSON ফাইল ও আউটপুট ফাইল
json_file = "Bangla Channel.json"
output_file = "Combined_Live_TV.m3u"

# 🔸 হেডার
buf = StringIO()
buf.write("#EXTM3U\n\n")

# Precompiled regex
re_group_title = re.compile(r'group-title="(.*?)"')
EXTINF_PREFIX = "#EXTINF:"

# 🔸 Step 1: সব M3U ফাইল একত্র করা
for file_name in m3u_files:
    if not os.path.exists(file_name):
        buf.write(f"# ⚠️ Missing file: {file_name}\n")
        continue

    group_name = os.path.splitext(os.path.basename(file_name))[0]

    try:
        with open(file_name, "r", encoding="utf-8", errors="replace") as f:
            lines = [l.strip() for l in f if l.strip()]
    except Exception as e:
        buf.write(f"# ⚠️ Error reading {file_name}: {e}\n")
        continue

    if not lines:
        continue

    buf.write(f"\n# 📁 Source: {file_name}\n")

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]

        if line.startswith(EXTINF_PREFIX):
            # group-title যোগ/রিপ্লেস
            if 'group-title="' in line:
                line = re_group_title.sub(f'group-title="{group_name}"', line)
            else:
                parts = line.split(",", 1)
                if len(parts) == 2:
                    line = f'{parts[0]} group-title="{group_name}",{parts[1]}'

            # পরবর্তী লাইনগুলো একত্র করা (referrer/origin/url)
            segment_lines = [line]
            j = i + 1
            while j < n and not lines[j].startswith(EXTINF_PREFIX):
                segment_lines.append(lines[j])
                j += 1

            buf.write("\n".join(segment_lines) + "\n")
            i = j
        else:
            i += 1

# 🔸 Step 2: JSON ফাইল থেকে ডেটা যোগ করা
if os.path.exists(json_file):
    try:
        with open(json_file, "r", encoding="utf-8") as jf:
            json_data = json.load(jf)

        json_group_name = os.path.splitext(os.path.basename(json_file))[0]
        buf.write(f"\n# 📁 Source: {json_file}\n")

        for channel_name, info in (json_data or {}).items():
            logo = info.get("tvg_logo", "")
            links = info.get("links", [])
            url = ""
            if isinstance(links, list) and links:
                url = (links[0] or {}).get("url", "")
            if not url:
                continue

            buf.write(
                f'#EXTINF:-1 tvg-logo="{logo}" group-title="{json_group_name}",{channel_name}\n{url}\n'
            )

    except Exception as e:
        buf.write(f"# ⚠️ Error reading {json_file}: {e}\n")
else:
    buf.write(f"# ⚠️ Missing JSON file: {json_file}\n")

# 🔸 Step 3: সর্বশেষ আপডেট টাইম (Bangladesh Time)
bd_time = datetime.utcnow() + timedelta(hours=6)
buf.write(f"\n# ✅ Last updated: {bd_time.strftime('%Y-%m-%d %H:%M:%S')} Bangladesh Time\n")

# 🔸 Step 4: আউটপুট লিখে দাও
try:
    with open(output_file, "w", encoding="utf-8") as out:
        out.write(buf.getvalue())
    print("✅ Combined_Live_TV.m3u created successfully with referrer/origin support (no duplicate filter)!")
except Exception as e:
    print(f"⚠️ Error writing output file: {e}")
