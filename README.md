# YouTube Playlist Downloader (Python Tkinter GUI)

A user-friendly desktop application built with Python's Tkinter and yt-dlp for effortlessly downloading entire YouTube playlists or selected video ranges. This GUI tool simplifies the process of saving your favorite educational content, music, or any YouTube playlist directly to your local machine, with options for video or audio-only downloads.

## ✨ Features

* Intuitive GUI: A clean and straightforward graphical interface built with Tkinter (enhanced with ttkbootstrap for a modern look).

* Playlist Download: Download all videos from a given YouTube playlist.

* Selective Download: Option to download specific videos within a playlist by specifying start and end indices.

* Audio-Only Mode: Convert and download videos as high-quality MP3 files (requires FFmpeg).

* Custom Download Path: Choose any directory on your computer to save your downloaded content.

* Real-time Progress: Live updates on download status and progress for each video.

* Robust Backend: Leverages yt-dlp, a powerful and actively maintained YouTube downloader.

* Error Handling: Basic error handling to notify users of issues during download.

## 🚀 Getting Started

To run this application, you'll need Python installed on your system, along with a few libraries and FFmpeg.

## 1. Prerequisites:

* Python 3.7+: Download from python.org.

* FFmpeg: Essential for merging video/audio streams and converting to MP3.
  * Download from ffmpeg.org/download.html.
  * Crucially, add the directory containing ffmpeg.exe (or the ffmpeg executable) to your system's PATH environmental variable. (If you encounter "no bin folder" issues, ensure you add the directory where ffmpeg.exe directly resides.)

## 2. Installation:

## Clone this repository or download the source code:

```bash
Bash

git clone https://github.com/sahannanasith/Youtube-Playlist-Downloader.git 
cd YOUR_REPO_NAME 
```

## Install the required Python libraries:

```bash
Bash

pip install yt-dlp ttkbootstrap
```

## 3. Running the Application:

```bash
Bash

python main.py
```

📸 Screenshots 



