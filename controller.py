

import threading
import tkinter as tk
import os
from pytube import YouTube

class Controller:
    def __init__(self, view):
        self.view = view

        self.view.url_button.configure(command=lambda:self.update_formats())
        self.view.download_button.configure(command=lambda:self.download())
        self.view.progress_bar.configure(value=0)

    def download(self):
        url = self.view.url_entry.get()
        format = self.view.format_combobox.get()
        itag = format.split('-')[-1].strip()  # Extract the itag from the format string
        path = self.view.path_entry.get()
        #check if the video is already downloaded
        
        # Pass the download to a thread
        thread = threading.Thread(target=lambda: self.download_thread(url, itag, path))
        thread.start()

    def download_thread(self, url, itag, path):
        self.model = YouTube(url)
        self.model.register_on_progress_callback(self.on_progress)
        self.model.streams.get_by_itag(itag).download(path)
        tk.messagebox.showinfo("Download", "Download completed")
        self.view.progress_bar.configure(value=0)


    def update_formats(self):
        url = self.view.url_entry.get()
        self.model = YouTube(url)
        self.model.register_on_progress_callback(self.on_progress)
        self.model.streams.filter(progressive=True)
        list = []

        # Get resolution and mime_type from the streams
        for stream in self.model.streams:
            list.append(f"{stream.resolution} - {stream.mime_type} - {stream.itag}")

        self.view.format_combobox.configure(values=list) 
        self.view.format_combobox.set(list[0])
        self.view.format_combobox.configure(state="normal")

    def on_progress(self, stream, chunk, bytes_remaining):
        """Callback function"""
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        pct_completed = bytes_downloaded / total_size * 100
        print(f"Status: {round(pct_completed, 2)} %")
        self.view.progress_bar.configure(value=pct_completed)

