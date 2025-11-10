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
    "KALKATA.m3u"
]

sports_file = "Sports.m3u"
json_file = "Bangla Channel.json"

output_file = "Combined_Live_TV.m3u"

# -----------------------------
# 🔹 Helper
# -----------------------------
def clean_name(name):
    """চ্যানেলের নাম ক্লিন করে lowercase রিটার্ন করে"""
    return re.sub(r'\s+', ' ', name.strip().lower())

channels = {}

# -----------------------------
# 🔹 Add Channel
# -----------------------------
def add_channel(name, url, logo, group, ref=None, origin=None):
    cname = clean_name(name)
    if not url.startswith("http"):
        return  # ⚠️ Offline লিংক স্কিপ করবে

    data = {
        "name": name.strip(),
        "url": url.strip(),
        "logo": logo.strip(),
        "group": group.strip()
    }
    # ✅ শুধুমাত্র যদি থাকে
    if ref:
        data["ref"] = ref.strip()
    if origin:
        data["origin"] = origin.strip()

    # ✅ আগেরটা রিপ্লেস করবে (ডুপলিকেট রাখবে না)
    channels[cname] = data


# -----------------------------
# 🔹 Function: Load a single M3U file
# -----------------------------
def load_m3u(file_name):
    """একটি m3u ফাইল থেকে Referrer/Origin collect করে শুধুমাত্র ওই ফাইলের চ্যানেলগুলোতে apply করবে"""
    if not os.path.exists(file_name):
        print(f"⚠️ Missing file: {file_name}")
        return

    has_ref = has_origin = False
    with open(file_name, "r", encoding="utf-8-sig") as f:
        content = f.read()
        if "#EXTVLCOPT:http-referrer=" in content:
            has_ref = True
        if "#EXTVLCOPT:http-origin=" in content:
            has_origin = True

    group_name = os.path.splitext(os.path.basename(file_name))[0]
    with open(file_name, "r", encoding="utf-8-sig") as f:
        lines = f.read().splitlines()

    current_name = ""
    current_logo = ""
    ref = origin = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("#EXTINF"):
            logo_match = re.search(r'tvg-logo="(.*?)"', line)
            current_logo = logo_match.group(1) if logo_match else ""
            if "," in line:
                current_name = line.split(",", 1)[1].strip()
        elif line.startswith("#EXTVLCOPT:http-referrer="):
            ref = line.replace("#EXTVLCOPT:http-referrer=", "").strip()
        elif line.startswith("#EXTVLCOPT:http-origin="):
            origin = line.replace("#EXTVLCOPT:http-origin=", "").strip()
        elif line.startswith("http"):
            add_channel(
                current_name,
                line,
                current_logo,
                group_name,
                ref if has_ref else None,
                origin if has_origin else None
            )
            ref = origin = None


# -----------------------------
# 🔹 Load All M3U Files
# -----------------------------
for f in m3u_files:
    load_m3u(f)


# -----------------------------
# 🔹 Load Sports.m3u (Ref/Origin as per Sports file)
# -----------------------------
sports_blocks = []
if os.path.exists(sports_file):
    with open(sports_file, "r", encoding="utf-8-sig") as f:
        lines = f.read().splitlines()

    current_block = []
    ref = origin = ""
    current_name = ""
    current_logo = ""

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("#EXTINF"):
            logo_match = re.search(r'tvg-logo="(.*?)"', line)
            current_logo = logo_match.group(1) if logo_match else ""
            current_name = line.split(",", 1)[1].strip() if "," in line else "Unknown Channel"
        elif line.startswith("#EXTVLCOPT:http-referrer="):
            ref = line.replace("#EXTVLCOPT:http-referrer=", "").strip()
        elif line.startswith("#EXTVLCOPT:http-origin="):
            origin = line.replace("#EXTVLCOPT:http-origin=", "").strip()
        elif line.startswith("http"):
            add_channel(current_name, line, current_logo, "Sports", ref, origin)
            sports_blocks.append("\n".join(current_block + [line]))
            current_block = []
            ref = origin = ""
        current_block.append(line)
else:
    print(f"⚠️ Missing file: {sports_file}")


# -----------------------------
# 🔹 Load JSON
# -----------------------------
if os.path.exists(json_file):
    try:
        with open(json_file, "r", encoding="utf-8-sig") as jf:
            data = json.load(jf)
        group = os.path.splitext(os.path.basename(json_file))[0]
        for ch_name, info in data.items():
            logo = info.get("tvg_logo", "")
            links = info.get("links", [])
            if isinstance(links, list) and links:
                url = links[0].get("url", "")
                if url:
                    add_channel(ch_name, url, logo, group)
    except Exception as e:
        print(f"❌ JSON Error in {json_file}: {e}")
else:
    print(f"⚠️ Missing file: {json_file}")


# -----------------------------
# 🔹 Write Combined Output
# -----------------------------
def write_combined_m3u(file_path, data_dict, sports_blocks):
    content = "#EXTM3U\n\n"

    if sports_blocks:
        content += "# ---------- 🏏 SPORTS CHANNELS ----------\n\n"
        for block in sports_blocks:
            content += block + "\n\n"

    content += "# ---------- 📺 OTHER CHANNELS ----------\n\n"

    for info in sorted(data_dict.values(), key=lambda x: x["name"].lower()):
        content += f'#EXTINF:-1 tvg-logo="{info["logo"]}" group-title="{info["group"]}",{info["name"]}\n'
        if "ref" in info:
            content += f'#EXTVLCOPT:http-referrer={info["ref"]}\n'
        if "origin" in info:
            content += f'#EXTVLCOPT:http-origin={info["origin"]}\n'
        content += f'{info["url"]}\n\n'

    bd_time = datetime.utcnow() + timedelta(hours=6)
    content += f"# ✅ Last updated: {bd_time.strftime('%Y-%m-%d %H:%M:%S')} BD Time\n"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


# -----------------------------
# 🔹 Final Write + Summary
# -----------------------------
write_combined_m3u(output_file, channels, sports_blocks)

print(f"\n✅ Combined_Live_TV.m3u created successfully with {len(channels)} channels.")
