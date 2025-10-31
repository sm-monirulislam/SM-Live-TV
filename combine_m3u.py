import os
from datetime import datetime, timedelta
import re

# যেসব m3u ফাইল একত্র হবে
m3u_files = [
    "Jagobd.m3u",
    "Aynaott.m3u",
    "SM All TV.m3u",
    "Toffee.m3u",
    "Fancode.m3u"
]

output_file = "Combined_Live_TV.m3u"
combined_content = "#EXTM3U\n\n"

for file_name in m3u_files:
    if not os.path.exists(file_name):
        combined_content += f"# ⚠️ Missing file: {file_name}\n"
        continue

    group_name = os.path.splitext(os.path.basename(file_name))[0]  # ফাইল নাম থেকে group title
    with open(file_name, "r", encoding="utf-8") as f:
        content = f.read().strip()

    if content.startswith("#EXTM3U"):
        content = content.replace("#EXTM3U", "").strip()

    # প্রতিটি #EXTINF লাইনের group-title পরিবর্তন করা
    new_lines = []
    for line in content.splitlines():
        if line.startswith("#EXTINF"):
            # আগের group-title থাকলে replace, না থাকলে নতুন করে add
            if 'group-title="' in line:
                line = re.sub(r'group-title="(.*?)"', f'group-title="{group_name}"', line)
            else:
                # group-title নেই, তাই নতুন করে যুক্ত করা
                parts = line.split(",", 1)
                if len(parts) == 2:
                    line = f'{parts[0]} group-title="{group_name}",{parts[1]}'
        new_lines.append(line)

    # ফলাফল একত্র করা
    combined_content += f"\n# 📁 Source: {file_name}\n" + "\n".join(new_lines) + "\n"

# বাংলাদেশ সময় অনুযায়ী সময় দেখানো
bd_time = datetime.utcnow() + timedelta(hours=6)
combined_content += f"\n# ✅ Last updated: {bd_time.strftime('%Y-%m-%d %H:%M:%S')} Bangladesh Time\n"

with open(output_file, "w", encoding="utf-8") as out:
    out.write(combined_content)

print("✅ Combined_Live_TV.m3u created with source-based group-titles successfully!")
