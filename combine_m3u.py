import os
import re
from datetime import datetime

OUTPUT = "Combined_Live_TV.m3u"

def extract_channels(text):
    """
    #EXTINF... (one line) followed by URL (next line) --> returns list of blocks
    """
    pattern = re.compile(r'(#EXTINF[^\n]*\n(?:https?://[^\s\n]+))', re.IGNORECASE)
    return pattern.findall(text)

def ensure_group_title(extinf_line, group_name):
    # যদি group-title থাকে তা replace, না থাকলে add
    if 'group-title=' in extinf_line:
        return re.sub(r'group-title="[^"]*"', f'group-title="{group_name}"', extinf_line)
    else:
        # insert group-title after #EXTINF:-1 (or after #EXTINF:<digits>)
        return re.sub(r'(#EXTINF:[^,]*)', r'\1 group-title="' + group_name + '"', extinf_line, count=1)

def main():
    files = [f for f in os.listdir('.') if f.lower().endswith('.m3u') and f != OUTPUT]
    files.sort()
    if not files:
        print("⚠️ কোনো .m3u ফাইল পাওয়া যায়নি।")
        return

    combined_lines = ["#EXTM3U\n"]
    total_channels = 0

    for fname in files:
        group = os.path.splitext(fname)[0].strip()
        print(f"Processing {fname} -> group: {group}")
        try:
            with open(fname, 'r', encoding='utf-8', errors='ignore') as fh:
                text = fh.read()
        except Exception as e:
            print(f"❌ Could not read {fname}: {e}")
            continue

        # ন্যূনতম পরিষ্কার: হেডার সরানো
        if text.strip().startswith("#EXTM3U"):
            text = text.replace("#EXTM3U", "", 1)

        channels = extract_channels(text)
        if not channels:
            # fallback: try to parse lines pairwise (EXTINF line then next line as url)
            lines = [ln for ln in text.splitlines() if ln.strip() != ""]
            i = 0
            while i < len(lines):
                line = lines[i]
                if line.strip().upper().startswith("#EXTINF"):
                    url = lines[i+1] if i+1 < len(lines) else ""
                    ch_block = f"{line}\n{url}"
                    channels.append(ch_block)
                    i += 2
                else:
                    i += 1

        for ch in channels:
            # ch is "#EXTINF... \nhttps://...."
            parts = ch.splitlines()
            if not parts:
                continue
            extinf = parts[0]
            rest = "\n".join(parts[1:]) if len(parts) > 1 else ""
            extinf = ensure_group_title(extinf, group)
            combined_lines.append(extinf.strip() + "\n" + rest.strip() + "\n")
            total_channels += 1

    # add timestamp comment
    combined_lines.append(f"\n# ✅ Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC\n")

    # write temp then replace only if changed (optional)
    new_content = "\n".join([ln.rstrip() for ln in combined_lines]).strip() + "\n"
    if os.path.exists(OUTPUT):
        with open(OUTPUT, 'r', encoding='utf-8', errors='ignore') as existing:
            old = existing.read()
    else:
        old = ""

    if new_content != old:
        with open(OUTPUT, 'w', encoding='utf-8') as out:
            out.write(new_content)
        print(f"✅ Wrote {OUTPUT} ({total_channels} channels from {len(files)} files).")
    else:
        print("✅ No change in combined file (content identical).")

if __name__ == "__main__":
    main()
