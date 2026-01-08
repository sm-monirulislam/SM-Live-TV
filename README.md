📺 Live TV Playlist Generator

Automatically generates M3U playlists for Live TV channels using GitHub Actions.
This project helps you host your M3U playlist on GitHub — always updated, clean, এবং offline links filtered.


---

🚀 Features

✔️ Auto-generate playlist.m3u

✔️ Offline/Dead link detection


🧪 Run Locally

python combine_playlist.py


---

🔄 GitHub Actions Workflow Example

name: 🔁 Auto Generate Live TV Playlist

on:
  schedule:
    - cron: "0 * * * *"   # Run every hour
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.x"

      - name: Install Dependencies
        run: pip install -r requirements.txt

      - name: Run Script
        run: python combine_playlist.py

      - name: Commit & Push
        run: |
          git config user.name "github-actions"
          git config user.email "github-actions@github.com"
          git add .
          git commit -m "Auto update playlist"
          git push


---

📡 Playlist URL

You can use your playlist link like:

https://raw.githubusercontent.com/sm-monirulislam/SM-Live-TV/refs/heads/main/Combined_Live_TV.m3u


# 🛡️ Credits

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&pause=100&color=FF2C10&background=00000000&width=400&lines=Made+By+Monirul+Islam)](https://git.io/typing-svg)


# 📝Note
* The following code is for educational purposes only. It demonstrates how to authenticate and stream IPTV. Do not use it for any illegal or harmful activities. If the code affects the revenue of the IPTV owners, please let me  and I will delete it.
* Please give me proper credit if you share this content. Otherwise, I will take it down.
* The codes of the repo are encrypted to ensure security. Please refrain from trying to run or deploy them 
* Due to geo-restriction, the IPTV content is only available in Bangladesh.




## CONNECT WITH US :


[![Instagram](https://img.shields.io/badge/WEBSITE-VISIT-yellow?style=for-the-badge&logo=blogger)](https://Monirul.github.io)
[![Instagram](https://img.shields.io/badge/TELEGRAM-CHANNEL-red?style=for-the-badge&logo=telegram)](https://t.me/monirul_Islam_SM)

#### 👤 Project Maintainer
**Monirul Islam**  
Maintained with ❤️ in Bangladesh 🇧🇩
# knowledged SM
## Special Thanks <span style="font-size:45px;">👇</span>


#### ℹ️ Project Info
- 🔄 Auto Updated via GitHub Actions  
- 📺 Live TV Playlist Support  
- 🐍 Powered by Python  
- 🇧🇩 Made in Bangladesh


<a href="#">
  <img 
    title="SM Monirul Islam"
    src="https://img.shields.io/badge/SM%20Monirul%20Islam-purple?style=for-the-badge&logo=github"
    alt="SM Monirul Islam"
  >
</a>

## Thanks For Using This Tool <span style="font-size:45px;">😘</span> <span style="font-size:45px;">😍</span>
