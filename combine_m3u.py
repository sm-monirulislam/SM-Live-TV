import os
from datetime import datetime, timedelta

# ইনপুট ফাইলগুলোর তালিকা
m3u_files = [
    "jagobd.m3u",
    "aynaott.m3u",
    "SM All TV.m3u",
    "toffee.m3u",
    "fancode.m3u"
]

output_file = "Combined_Live_TV.m3u"

combined_content = "#EXTM3U\n\n"

for file_name in m3u_files:
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content.startswith("#EXTM3U"):
                content = content.replace("#EXTM3U", "").strip()
            combined_content += f"\n# 📁 Source: {file_name}\n{content}\n"
    else:
        combined_content += f"\n# ⚠️ Missing file: {file_name}\n"

# বাংলাদেশ সময় অনুযায়ী টাইমস্ট্যাম্প
bd_time = datetime.utcnow() + timedelta(hours=6)
combined_content += f"\n# ✅ Last updated: {bd_time.strftime('%Y-%m-%d %H:%M:%S')} Bangladesh Time\n"

with open(output_file, "w", encoding="utf-8") as out:
    out.write(combined_content)

print("✅ Combined_Live_TV.m3u created/updated successfully!")
