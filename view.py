import customtkinter as ct
from customtkinter import filedialog
from tkinter import ttk

class DownloaderApp(ct.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("YT Downloader")

        # Setting up the theme
        ct.set_appearance_mode("dark")
        

        self.url_label = ct.CTkLabel(self, text="URL :")
        self.url_label.grid(row=0, column=0, padx=10, pady=10)
        self.url_entry = ct.CTkEntry(self)
        self.url_entry.grid(row=0, column=1, padx=10, pady=10)
        self.url_button = ct.CTkButton(self, text="Check Url")
        self.url_button.grid(row=0, column=2, padx=10, pady=10)


        self.format_label = ct.CTkLabel(self, text="Format :")
        self.format_label.grid(row=1, column=0, padx=10, pady=10)
        self.format_combobox = ct.CTkComboBox(self,state="disabled", values=[""])
        self.format_combobox.grid(row=1, column=1, padx=10, pady=10,columnspan=2, sticky="we")

        self.path_label = ct.CTkLabel(self, text="Path :")
        self.path_label.grid(row=2, column=0, padx=10, pady=10)
        self.path_entry = ct.CTkEntry(self)
        self.path_entry.grid(row=2, column=1, padx=10, pady=10)

        self.browse_button = ct.CTkButton(self, text="Browse", command=self.open_directory)
        self.browse_button.grid(row=2, column=2, padx=10, pady=10)

        self.download_button = ct.CTkButton(self, text="Download", state="disabled")
        self.download_button.grid(row=4, column=0, padx=10, pady=10, columnspan=3, sticky="we")

        self.progress_bar = ttk.Progressbar(self, length=200)
        self.progress_bar.grid(row=5, column=0,  padx=10, pady=10, sticky="we",columnspan=3)

    def open_directory(self):
        directory = filedialog.askdirectory()
        self.path_entry.delete(0, "end")
        self.path_entry.insert(0, directory)
        self.download_button.configure(state="normal")