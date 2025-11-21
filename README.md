<h1 align="center">🚀 SM Live TV — Auto Playlist Update System</h1>

<p align="center">
  <b>Fully automated M3U playlist updater powered by GitHub Actions ⚙️</b><br>
  Fancode 🏏 + CricHD 🎬 playlists update automatically every 10 minutes 🔁
</p>

---

## 🟢 Live Workflow Status

| Workflow | Status |
|-----------|--------|
| 🎯 **Main Orchestrator** | ![Main Orchestrator](https://github.com/sm-monirulislam/SM-Live-TV/actions/workflows/main_orchestrator.yml/badge.svg) |
| ⚙️ **Fancode Auto Update** | ![Fancode Update](https://github.com/sm-monirulislam/SM-Live-TV/actions/workflows/auto_update.yml/badge.svg) |
| 🏏 **CricHD Auto Update** | ![CricHD Update](https://github.com/sm-monirulislam/SM-Live-TV/actions/workflows/CricHD_update_playlist.yml/badge.svg) |

> 🟢 = Running successfully | 🔴 = Error or failed | ⏳ = In progress

---

## ⚙️ Workflow Overview

বর্তমানে সিস্টেমে মোট **৩টি workflow** আছে 👇

| 🔢 | 📜 Workflow File | ⚡ কাজ |
|----|------------------|--------|
| 1️⃣ | `.github/workflows/main_orchestrator.yml` | 🎯 প্রতি **১০ মিনিটে** বা ম্যানুয়ালি `Fancode` ও `CricHD` workflow ট্রিগার করে |
| 2️⃣ | `.github/workflows/auto_update.yml` | ⚙️ `Fancode.m3u` playlist আপডেট করে |
| 3️⃣ | `.github/workflows/CricHD_update_playlist.yml` | 🏏 `Sports.m3u` playlist তৈরি করে |

---

## 🔄 Execution Flow (How It Works)

```text
main_orchestrator.yml
   ├── auto_update.yml             →  Fancode.m3u আপডেট
   └── CricHD_update_playlist.yml  →  Sports.m3u আপডেট
