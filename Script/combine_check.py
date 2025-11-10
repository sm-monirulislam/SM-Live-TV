import os
import json
import re
from datetime import datetime, timedelta

# -----------------------------
# 🔹 Input Files
# -----------------------------
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
output_file = "Combined_Live_TV.m3u"
duplicate_file = "Duplicate.m3u"

# -----------------------------
# 🔹 Helper: Clean Channel Name
# -----------------------------
def clean_name(name):
    """Channel name normalize করে lowercase এ নেয়"""
    return re.sub(r'\s+', ' ', name.strip().lower())

# -----------------------------
# 🔹 Step 1: Combine All M3U + JSON
# -----------------------------
channels = {}
duplicates = {}

def add_channel(name, url, logo, group):
    cname = clean_name(name)
    data = {
        "name": name.strip(),
        "url": url.strip(),
        "logo": logo.strip(),
        "group": group.strip()
    }

    if cname in channels:
        # যদি একই নামের channel আগে থেকেই থাকে = duplicate
        if cname not in duplicates:
            duplicates[cname] = [channels[cname]]  # প্রথমটি সংরক্ষণ করো
        duplicates[cname].append(data)
    else:
        channels[cname] = data


# -----------------------------
# 🔹 Load M3U Files
# -----------------------------
for file_name in m3u_files:
    if not os.path.exists(file_name):
        print(f"⚠️ Missing file: {file_name}")
        continue

    group_name = os.path.splitext(os.path.basename(file_name))[0]
    with open(file_name, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    current_logo = ""
    current_name = ""
    for line in lines:
        if line.startswith("#EXTINF"):
            logo_match = re.search(r'tvg-logo="(.*?)"', line)
            current_logo = logo_match.group(1) if logo_match else ""
            if "," in line:
                current_name = line.split(",", 1)[1].strip()
        elif line.startswith("http"):
            add_channel(current_name, line, current_logo, group_name)


# -----------------------------
# 🔹 Load JSON File
# -----------------------------
if os.path.exists(json_file):
    with open(json_file, "r", encoding="utf-8") as jf:
        try:
            json_data = json.load(jf)
            json_group_name = os.path.splitext(os.path.basename(json_file))[0]
            for channel_name, info in json_data.items():
                logo = info.get("tvg_logo", "")
                links = info.get("links", [])
                if links and isinstance(links, list):
                    url = links[0].get("url", "")
                    if url:
                        add_channel(channel_name, url, logo, json_group_name)
        except Exception as e:
            print(f"⚠️ Error reading {json_file}: {e}")
else:
    print(f"⚠️ Missing JSON file: {json_file}")


# -----------------------------
# 🔹 Step 2: Write Combined File
# -----------------------------
def write_m3u(file_path, data_dict):
    content = "#EXTM3U\n\n"
    for info in data_dict.values():
        content += (
            f'#EXTINF:-1 tvg-logo="{info["logo"]}" group-title="{info["group"]}",{info["name"]}\n'
            f'{info["url"]}\n'
        )
    bd_time = datetime.utcnow() + timedelta(hours=6)
    content += f"\n# ✅ Last updated: {bd_time.strftime('%Y-%m-%d %H:%M:%S')} Bangladesh Time\n"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

# Combined (unique)
write_m3u(output_file, channels)

# -----------------------------
# 🔹 Step 3: Write Duplicate Channels (if any)
# -----------------------------
if duplicates:
    print(f"⚠️ Found {len(duplicates)} duplicate channel names.")
    dup_content = "#EXTM3U\n\n"
    for cname, dup_list in duplicates.items():
        dup_content += f"# 🔁 Duplicate: {dup_list[0]['name']}\n"
        for info in dup_list:
            dup_content += (
                f'#EXTINF:-1 tvg-logo="{info["logo"]}" group-title="{info["group"]}",{info["name"]}\n'
                f'{info["url"]}\n'
            )
        dup_content += "\n"
    bd_time = datetime.utcnow() + timedelta(hours=6)
    dup_content += f"# ⚠️ Duplicate list generated: {bd_time.strftime('%Y-%m-%d %H:%M:%S')} Bangladesh Time\n"

    with open(duplicate_file, "w", encoding="utf-8") as f:
        f.write(dup_content)
else:
    with open(duplicate_file, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n\n# ✅ No duplicate channels found.\n")

# -----------------------------
# 🔹 Step 4: Summary
# -----------------------------
print("✅ Combined_Live_TV.m3u created successfully.")
if duplicates:
    print(f"⚠️ Duplicate.m3u saved with {len(duplicates)} duplicate channel entries.")
else:
    print("✅ No duplicate channels found.")
