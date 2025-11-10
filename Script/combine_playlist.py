import os
import json
from datetime import datetime, timedelta
import re

# 🔹 যেসব M3U ফাইল একত্র হবে
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

# 🔹 JSON ফাইলের নাম ও আউটপুট ফাইল
json_file = "Bangla Channel.json"
output_file = "Combined_Live_TV.m3u"

# 🔸 শুরুতে হেডার লাইন
combined_content = "#EXTM3U\n\n"

# ✅ ডুপ্লিকেট চ্যানেল রোধ করার জন্য একটি সেট তৈরি
added_channels = set()

# 🔸 Step 1: সব M3U ফাইল একত্র করা
for file_name in m3u_files:
    if not os.path.exists(file_name):
        combined_content += f"# ⚠️ Missing file: {file_name}\n"
        continue

    group_name = os.path.splitext(os.path.basename(file_name))[0]

    try:
        with open(file_name, "r", encoding="utf-8") as f:
            content = f.read().strip()
    except Exception as e:
        combined_content += f"# ⚠️ Error reading {file_name}: {e}\n"
        continue

    # যদি ফাইল "#EXTM3U" দিয়ে শুরু হয়, সেটা সরিয়ে দেই
    if content.startswith("#EXTM3U"):
        content = content.replace("#EXTM3U", "").strip()

    combined_content += f"\n# 📁 Source: {file_name}\n"

    lines = content.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("#EXTINF"):
            # group-title পরিবর্তন বা যোগ করা
            if 'group-title="' in line:
                line = re.sub(r'group-title="(.*?)"', f'group-title="{group_name}"', line)
            else:
                parts = line.split(",", 1)
                if len(parts) == 2:
                    line = f'{parts[0]} group-title="{group_name}",{parts[1]}'

            # চ্যানেল নাম বের করা
            channel_name = line.split(",", 1)[-1].strip()
            if channel_name in added_channels:
                continue  # ডুপ্লিকেট চ্যানেল স্কিপ করো
            added_channels.add(channel_name)

            # URL যোগ করা (পরবর্তী লাইন)
            if i + 1 < len(lines):
                url = lines[i + 1].strip()
                combined_content += f"{line}\n{url}\n"

# 🔸 Step 2: JSON ফাইল থেকে ডেটা যোগ করা
if os.path.exists(json_file):
    try:
        with open(json_file, "r", encoding="utf-8") as jf:
            json_data = json.load(jf)
        json_group_name = os.path.splitext(os.path.basename(json_file))[0]

        combined_content += f"\n# 📁 Source: {json_file}\n"

        for channel_name, info in json_data.items():
            if channel_name in added_channels:
                continue  # ডুপ্লিকেট স্কিপ

            logo = info.get("tvg_logo", "")
            links = info.get("links", [])
            url = ""
            if links and isinstance(links, list) and len(links) > 0:
                url = links[0].get("url", "")
            if not url:
                continue  # URL না থাকলে স্কিপ

            combined_content += (
                f'#EXTINF:-1 tvg-logo="{logo}" group-title="{json_group_name}",{channel_name}\n{url}\n'
            )
            added_channels.add(channel_name)

    except Exception as e:
        combined_content += f"# ⚠️ Error reading {json_file}: {e}\n"
else:
    combined_content += f"# ⚠️ Missing JSON file: {json_file}\n"

# 🔸 Step 3: সর্বশেষ আপডেট টাইম (Bangladesh Time)
bd_time = datetime.utcnow() + timedelta(hours=6)
combined_content += f"\n# ✅ Last updated: {bd_time.strftime('%Y-%m-%d %H:%M:%S')} Bangladesh Time\n"

# 🔸 Step 4: আউটপুট ফাইল সংরক্ষণ
try:
    with open(output_file, "w", encoding="utf-8") as out:
        out.write(combined_content)
    print("✅ Combined_Live_TV.m3u created successfully!")
except Exception as e:
    print(f"⚠️ Error writing output file: {e}")
