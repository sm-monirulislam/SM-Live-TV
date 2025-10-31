import os
import re

def combine_m3u_files(output_file="Combined_Live_TV.m3u"):
    # সব m3u ফাইল সংগ্রহ (output বাদে)
    m3u_files = [f for f in os.listdir('.') if f.endswith('.m3u') and f != output_file]

    if not m3u_files:
        print("⚠️ কোনো .m3u ফাইল পাওয়া যায়নি!")
        return

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write("#EXTM3U\n\n")

        for file in m3u_files:
            group_name = os.path.splitext(file)[0].strip()
            print(f"📂 Processing: {file} → group: {group_name}")

            with open(file, 'r', encoding='utf-8', errors='ignore') as infile:
                content = infile.read()

                # প্রতিটি চ্যানেল ব্লক (#EXTINF + URL)
                channels = re.findall(r'(#EXTINF[^\n]+\nhttps?:\/\/[^\n]+)', content)

                for ch in channels:
                    # আগের group-title replace করা
                    ch = re.sub(r'group-title="[^"]*"', f'group-title="{group_name}"', ch)
                    # group-title না থাকলে যোগ করা
                    if 'group-title=' not in ch:
                        ch = ch.replace('#EXTINF:-1', f'#EXTINF:-1 group-title="{group_name}"')

                    outfile.write(ch.strip() + '\n\n')

        print(f"✅ Combined {len(m3u_files)} files into {output_file}")

if __name__ == "__main__":
    combine_m3u_files()
