import os
import re

def combine_m3u_files(output_file="Combined_Live_TV.m3u"):
    # সব m3u ফাইল সংগ্রহ
    m3u_files = [f for f in os.listdir('.') if f.endswith('.m3u') and f != output_file]

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write("#EXTM3U\n")
        for file in m3u_files:
            group_name = os.path.splitext(file)[0].strip()  # যেমন Aynaott.m3u → Aynaott
            with open(file, 'r', encoding='utf-8', errors='ignore') as infile:
                content = infile.read()

                # প্রতিটি চ্যানেল ব্লক বের করা
                channels = re.findall(r'(#EXTINF[^\n]+\nhttps?:\/\/[^\n]+)', content)
                for ch in channels:
                    # group-title পরিবর্তন বা অ্যাড করা
                    ch = re.sub(r'group-title="[^"]*"', f'group-title="{group_name}"', ch)
                    if 'group-title=' not in ch:
                        ch = ch.replace('#EXTINF:-1', f'#EXTINF:-1 group-title="{group_name}"')
                    outfile.write(ch.strip() + '\n')
        print(f"✅ Combined {len(m3u_files)} files into {output_file}")

if __name__ == "__main__":
    combine_m3u_files()
