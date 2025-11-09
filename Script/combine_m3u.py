import os
import json
from datetime import datetime, timedelta
import re

# যেসব m3u ফাইল একত্র হবে
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

# 🔹 JSON ফাইলের নাম
json_file = "Bangla Channel.json"

output_file = "Combined_Live_TV.m3u"
combined_content = "#EXTM3U\n\n"

# 🔸 Step 1: সব M3U ফাইল একত্র করা
for file_name in m3u_files:
    if not os.path.exists(file_name):
        combined_content += f"# ⚠️ Missing file: {file_name}\n"
        continue

    group_name = os.path.splitext(os.path.basename(file_name))[0]
    with open(file_name, "r", encoding="utf-8") as f:
        content = f.read().strip()

    if content.startswith("#EXTM3U"):
        content = content.replace("#EXTM3U", "").strip()

    new_lines = []
    for line in content.splitlines():
        if line.startswith("#EXTINF"):
            if 'group-title="' in line:
                line = re.sub(r'group-title="(.*?)"', f'group-title="{group_name}"', line)
            else:
                parts = line.split(",", 1)
                if len(parts) == 2:
                    line = f'{parts[0]} group-title="{group_name}",{parts[1]}'
        new_lines.append(line)

    combined_content += f"\n# 📁 Source: {file_name}\n" + "\n".join(new_lines) + "\n"

# 🔸 Step 2: JSON ফাইল থেকে ডেটা যোগ করা (group-title = JSON ফাইলের নাম)
if os.path.exists(json_file):
    with open(json_file, "r", encoding="utf-8") as jf:
        try:
            json_data = json.load(jf)
            json_group_name = os.path.splitext(os.path.basename(json_file))[0]  # e.g. "Bangla Channel"
            combined_content += f"\n# 📁 Source: {json_file}\n"

            # ✅ JSON পড়া তোমার ফরম্যাট অনুযায়ী
            for channel_name, info in json_data.items():
                logo = info.get("tvg_logo", "")
                links = info.get("links", [])
                if links and isinstance(links, list):
                    url = links[0].get("url", "")
                else:
                    url = ""

                if url:
                    combined_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{json_group_name}",{channel_name}\n{url}\n'
        except Exception as e:
            combined_content += f"# ⚠️ Error reading {json_file}: {e}\n"
else:
    combined_content += f"# ⚠️ Missing JSON file: {json_file}\n"

# 🔸 Step 3: সর্বশেষ আপডেট টাইম
bd_time = datetime.utcnow() + timedelta(hours=6)
combined_content += f"\n# ✅ Last updated: {bd_time.strftime('%Y-%m-%d %H:%M:%S')} Bangladesh Time\n"

# 🔸 Step 4: ফাইনাল আউটপুট সংরক্ষণ
with open(output_file, "w", encoding="utf-8") as out:
    out.write(combined_content)

print("✅ Combined_Live_TV.m3u created successfully with JSON group-title = script name!")
