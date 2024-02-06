

import threading
import tkinter as tk
import os
from pytube import YouTube

class Controller:
    def __init__(self, view):
        self.view = view

        self.view.url_button.configure(command=lambda:self.update_CBB())
        self.view.download_button.configure(command=lambda:self.download())
        self.view.download_subtitle_button.configure(command=lambda:self.download_subtitle())
        self.view.progress_bar.configure(value=0)

    def download(self):
        url = self.view.url_entry.get()
        format = self.view.format_combobox.get()
        itag = format.split('-')[-1].strip()  # Extract the itag from the format string
        path = self.view.path_entry.get()
        subtitle = self.view.subtitle_combobox.get().split('-')[-1].strip()
        #check if the video is already downloaded
        
        # Pass the download to a thread
        thread = threading.Thread(target=lambda: self.download_thread(url, itag, path))
        thread.start()
        if subtitle != "":
            thread_sub = threading.Thread(target=lambda: self.download_subtitle_thread(url, subtitle, path))
            thread_sub.start()
        

    def download_subtitle(self):
        url = self.view.url_entry.get()
        subtitle = self.view.subtitle_combobox.get().split('-')[-1].strip()
        path = self.view.path_entry.get()
        # Pass the download to a thread
        thread = threading.Thread(target=lambda: self.download_subtitle_thread(url, subtitle, path))
        thread.start()
        

    def download_thread(self, url, itag, path):
        
        self.model.register_on_progress_callback(self.on_progress)
        self.model.streams.get_by_itag(itag).download(path)
        tk.messagebox.showinfo("Download", "Download completed")
        self.view.progress_bar.configure(value=0)

    def download_subtitle_thread(self, url, subtitle, path):
        try:
            self.model.register_on_progress_callback(self.on_progress)
            print(f"Downloading subtitle '{subtitle}' for video '{self.model.title}' to '{path}/{self.model.title}.srt'")
            self.model.captions[subtitle].download(f"{path}/{self.model.title}.srt")
            tk.messagebox.showinfo("Download", "Download completed")
            self.view.progress_bar.configure(value=0)
        except KeyError:
            print(f"No caption found for language code: {subtitle}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def update_CBB(self):
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

        list = []

        for caption in self.model.captions:
            list.append(f"{caption.name} - {caption.code}")

        self.view.subtitle_combobox.configure(values=list) 
        self.view.subtitle_combobox.set(list[0])
        self.view.subtitle_combobox.configure(state="normal")
        

    def on_progress(self, stream, chunk, bytes_remaining):
        """Callback function"""
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        pct_completed = bytes_downloaded / total_size * 100
        print(f"Status: {round(pct_completed, 2)} %")
        self.view.progress_bar.configure(value=pct_completed)

