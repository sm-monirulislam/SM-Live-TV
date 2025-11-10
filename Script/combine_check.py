import os
import json
import re
import requests
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
offline_file = "offline.m3u"
log_file = "invalid_links.log"

# -----------------------------
# 🔹 Helper: Check if stream link is valid
# -----------------------------
def is_stream_alive(url):
    try:
        if not url.startswith("http"):
            return False
        response = requests.head(url, timeout=5, allow_redirects=True)
        return response.status_code == 200
    except:
        return False

# -----------------------------
# 🔹 Helper: Clean & Normalize Channel Name
# -----------------------------
def clean_name(name):
    return re.sub(r'\s+', ' ', name.strip().lower())

# -----------------------------
# 🔹 Step 1: Merge all M3U files
# -----------------------------
combined_channels = {}

def add_channel(name, url, logo, group):
    cname = clean_name(name)
    if cname not in combined_channels:  # avoid duplicates
        combined_channels[cname] = {
            "name": name.strip(),
            "url": url.strip(),
            "logo": logo.strip(),
            "group": group.strip()
        }

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
# 🔹 Step 2: Add channels from JSON
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
# 🔹 Step 3: Validate Stream Links
# -----------------------------
print("\n🔍 Checking all stream links (please wait)...\n")

valid_channels = {}
offline_channels = {}
log_entries = []

for cname, info in combined_channels.items():
    url = info["url"]
    now = (datetime.utcnow() + timedelta(hours=6)).strftime("%Y-%m-%d %H:%M:%S")
    if is_stream_alive(url):
        valid_channels[cname] = info
        print(f"✅ LIVE: {info['name']}")
    else:
        offline_channels[cname] = info
        entry = f"[{now}] ❌ {info['name']} | {url}"
        log_entries.append(entry)
        print(f"❌ OFFLINE: {info['name']}")

# -----------------------------
# 🔹 Step 4: Generate Final M3U Files
# -----------------------------
def write_m3u(file_path, channels_dict):
    content = "#EXTM3U\n\n"
    for info in channels_dict.values():
        content += (
            f'#EXTINF:-1 tvg-logo="{info["logo"]}" group-title="{info["group"]}",{info["name"]}\n'
            f'{info["url"]}\n'
        )
    bd_time = datetime.utcnow() + timedelta(hours=6)
    content += f"\n# ✅ Last updated: {bd_time.strftime('%Y-%m-%d %H:%M:%S')} Bangladesh Time\n"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

write_m3u(output_file, valid_channels)
write_m3u(offline_file, offline_channels)

# -----------------------------
# 🔹 Step 5: Append Log File (time-based)
# -----------------------------
with open(log_file, "a", encoding="utf-8") as log:
    if log_entries:
        log.write("\n".join(log_entries) + "\n")
    else:
        now = (datetime.utcnow() + timedelta(hours=6)).strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{now}] ✅ All channels are working fine!\n")

# -----------------------------
# 🔹 Step 6: Summary
# -----------------------------
print("\n📊 Summary Report:")
print(f"✅ Total LIVE Channels: {len(valid_channels)}")
print(f"❌ Total OFFLINE Channels: {len(offline_channels)}")
print(f"💾 Saved to: {output_file} (LIVE)")
print(f"💾 Saved to: {offline_file} (OFFLINE)")
print(f"🪵 Log updated: {log_file}")
