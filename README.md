📺 Live TV Playlist Generator

Automatically generates M3U playlists for Live TV channels using GitHub Actions.
This project helps you host your M3U playlist on GitHub — always updated, clean, এবং offline links filtered.


---

🚀 Features

✔️ Auto-generate playlist.m3u

✔️ Offline/Dead link detection

✔️ Saves bad links to offline.m3u

✔️ Keeps previously offline links and checks again

✔️ Fully automated GitHub Action (runs every hour)

✔️ Clean, readable code structure

✔️ Works on any device (Smart TV, Android, iOS, PC)



---

📂 Project Structure

/
├── combine_playlist.py   # Main script to create playlist
├── sources/              # Your channel source files (TXT/M3U)
├── playlist.m3u          # Auto-generated output
├── offline.m3u           # Offline channel list
├── .github/workflows/
│   └── auto_generate.yml # GitHub Action workflow
└── README.md


---

⚙️ Installation 

1️⃣ Add your source M3U/TXT files

Put all URL list files inside:

/sources/

2️⃣ Make sure Python dependencies are installed

pip install -r requirements.txt


---

▶️ How It Works

1. Workflow runs every hour

GitHub Actions triggers the script:

combine_playlist.py

2. Script performs:

Load all channel URLs

Check if each link is online

Working links → added to playlist.m3u

Dead links → added to offline.m3u

Previously dead links are re-checked

After cleanup, final playlist is published


3. Updated playlist is pushed automatically

You will always have a fresh, clean, working playlist URL:

https://raw.githubusercontent.com/<username>/<repo>/main/playlist.m3u


---

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


---

💡 Tips

Use VPN if some channels are region-locked

Keep channel URLs updated

Avoid copyrighted premium sources

Use GitHub Actions free quota wisely



---

📝 License

This project is open-source under MIT License.


---

❤️ Contribution

Pull requests are always welcome!


---
