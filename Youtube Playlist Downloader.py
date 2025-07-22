import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import yt_dlp
import os

class YouTubePlaylistDownloader:
    def __init__(self, master):
        self.master = master
        master.title("YouTube Playlist Downloader")
        master.geometry("700x500") # Increased width for better layout
        master.resizable(False, False)

        # Apply a theme if ttkbootstrap is installed
        try:
            import ttkbootstrap as tb
            self.style = tb.Style("flatly") # You can try other themes like "cosmo", "flatly", "journal", "lumen", "minty", "united"
            self.master = self.style.master # Use the themed master
        except ImportError:
            print("ttkbootstrap not found. Using default Tkinter style.")
            self.style = ttk.Style()
            # Basic default theme settings for ttk if ttkbootstrap isn't used
            self.style.theme_use('clam')
            self.style.configure("TLabel", font=("Helvetica", 10))
            self.style.configure("TButton", font=("Helvetica", 10, "bold"))
            self.style.configure("TEntry", font=("Helvetica", 10))
            self.style.configure("TCheckbutton", font=("Helvetica", 10))
            self.style.configure("TProgressbar", thickness=20)


        # --- Input Frame ---
        input_frame = ttk.LabelFrame(master, text="Playlist Details", padding=15)
        input_frame.pack(padx=20, pady=10, fill="x", expand=True)

        ttk.Label(input_frame, text="Playlist URL:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.url_entry = ttk.Entry(input_frame, width=60)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(input_frame, text="Download Path:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.path_entry = ttk.Entry(input_frame, width=50)
        self.path_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.browse_button = ttk.Button(input_frame, text="Browse", command=self.browse_path)
        self.browse_button.grid(row=1, column=2, padx=5, pady=5)

        # Configure column weights for resizing
        input_frame.grid_columnconfigure(1, weight=1)

        # --- Options Frame ---
        options_frame = ttk.LabelFrame(master, text="Download Options", padding=15)
        options_frame.pack(padx=20, pady=10, fill="x", expand=True)

        self.audio_only_var = tk.BooleanVar(value=False)
        self.audio_only_checkbox = ttk.Checkbutton(options_frame, text="Download Audio Only (MP3)", variable=self.audio_only_var)
        self.audio_only_checkbox.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.start_index_var = tk.StringVar(value="")
        ttk.Label(options_frame, text="Start Index (Optional):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.start_index_entry = ttk.Entry(options_frame, width=10, textvariable=self.start_index_var)
        self.start_index_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.end_index_var = tk.StringVar(value="")
        ttk.Label(options_frame, text="End Index (Optional):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.end_index_entry = ttk.Entry(options_frame, width=10, textvariable=self.end_index_var)
        self.end_index_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        # --- Download Button ---
        self.download_button = ttk.Button(master, text="Start Download", command=self.start_download)
        self.download_button.pack(padx=20, pady=10)

        # --- Progress Frame ---
        progress_frame = ttk.LabelFrame(master, text="Download Progress", padding=15)
        progress_frame.pack(padx=20, pady=10, fill="x", expand=True)

        self.progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", mode="determinate", length=400)
        self.progress_bar.pack(pady=5, fill="x", expand=True)

        self.status_label = ttk.Label(progress_frame, text="Ready")
        self.status_label.pack(pady=5)

        self.current_video_label = ttk.Label(progress_frame, text="")
        self.current_video_label.pack(pady=5)

    def browse_path(self):
        directory = filedialog.askdirectory()
        if directory:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, directory)

    def start_download(self):
        playlist_url = self.url_entry.get().strip()
        download_path = self.path_entry.get().strip()
        audio_only = self.audio_only_var.get()
        start_index = self.start_index_var.get().strip()
        end_index = self.end_index_var.get().strip()

        if not playlist_url:
            messagebox.showerror("Error", "Please enter a YouTube playlist URL.")
            return
        if not download_path:
            messagebox.showerror("Error", "Please select a download path.")
            return

        if not os.path.isdir(download_path):
            try:
                os.makedirs(download_path)
            except OSError as e:
                messagebox.showerror("Error", f"Could not create directory: {e}")
                return

        self.download_button.config(state=tk.DISABLED)
        self.status_label.config(text="Starting download...")
        self.progress_bar.config(value=0, maximum=100)
        self.current_video_label.config(text="")

        # Run download in a separate thread to keep the GUI responsive
        threading.Thread(target=self.download_playlist, args=(playlist_url, download_path, audio_only, start_index, end_index)).start()

    def download_playlist(self, url, path, audio_only, start_index, end_index):
        try:
            ydl_opts = {
                'outtmpl': os.path.join(path, '%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s'),
                'progress_hooks': [self.my_hook],
                'ignoreerrors': True, # Continue downloading even if one video fails
                'verbose': False, # Set to True for more detailed console output from yt-dlp
                'ffmpeg_location': 'ffmpeg', # Assumes ffmpeg is in PATH
            }

            if audio_only:
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            else:
                ydl_opts['format'] = 'bestvideo+bestaudio/best'
                ydl_opts['merge_output_format'] = 'mp4'

            if start_index:
                try:
                    ydl_opts['playlist_start'] = int(start_index)
                except ValueError:
                    messagebox.showwarning("Warning", "Invalid Start Index. Ignoring.")
            if end_index:
                try:
                    ydl_opts['playlist_end'] = int(end_index)
                except ValueError:
                    messagebox.showwarning("Warning", "Invalid End Index. Ignoring.")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                if 'entries' in info_dict and info_dict['entries'] is not None:
                    total_videos = len(info_dict['entries'])
                    self.master.after(0, lambda: self.progress_bar.config(maximum=total_videos))
                    self.status_label.config(text=f"Found {total_videos} videos. Starting download...")

                    # Now actually download
                    ydl.download([url])
                else:
                    # Handle single video URL case or error
                    self.status_label.config(text="Downloading single video...")
                    self.master.after(0, lambda: self.progress_bar.config(maximum=100, value=0)) # Reset for single video
                    ydl.download([url])


            messagebox.showinfo("Success", "Playlist download complete!")
            self.status_label.config(text="Download Finished!")
            self.progress_bar.config(value=self.progress_bar['maximum'])

        except yt_dlp.utils.DownloadError as e:
            messagebox.showerror("Download Error", f"An error occurred during download: {e}")
            self.status_label.config(text="Download Failed!")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            self.status_label.config(text="Download Failed!")
        finally:
            self.download_button.config(state=tk.NORMAL)

    def my_hook(self, d):
        if d['status'] == 'downloading':
            filename = d.get('filename', 'Unknown File')
            _total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            _downloaded_bytes = d.get('downloaded_bytes', 0)

            if _total_bytes and _downloaded_bytes:
                percent = (_downloaded_bytes / _total_bytes) * 100
                self.master.after(0, lambda: self.progress_bar.config(value=percent)) # Update progress bar for current video
                self.master.after(0, lambda: self.status_label.config(text=f"Downloading: {filename} ({percent:.1f}%)"))
            else:
                self.master.after(0, lambda: self.status_label.config(text=f"Downloading: {filename}"))
                self.master.after(0, lambda: self.progress_bar.step(1)) # Indeterminate step if no total bytes
            
            # Update current video label for playlists
            if 'info_dict' in d and 'playlist_index' in d['info_dict'] and 'playlist_count' in d['info_dict']:
                playlist_index = d['info_dict']['playlist_index']
                playlist_count = d['info_dict']['playlist_count']
                title = d['info_dict'].get('title', 'Unknown Title')
                self.master.after(0, lambda: self.current_video_label.config(text=f"Video {playlist_index}/{playlist_count}: {title}"))
            elif 'info_dict' in d: # For single video
                title = d['info_dict'].get('title', 'Unknown Title')
                self.master.after(0, lambda: self.current_video_label.config(text=f"Downloading: {title}"))


        elif d['status'] == 'finished':
            filename = d.get('filename', 'Unknown File')
            self.master.after(0, lambda: self.status_label.config(text=f"Finished: {filename}"))
            # Update overall playlist progress if applicable.
            # For complex playlist progress, yt-dlp's hooks might need more sophisticated handling
            # to track individual video completion within a playlist.
            # For now, progress bar is mostly for the current video.

        elif d['status'] == 'error':
            self.master.after(0, lambda: self.status_label.config(text=f"Error: {d.get('filename', 'Unknown File')}"))

# Main application setup
if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubePlaylistDownloader(root)
    root.mainloop()
