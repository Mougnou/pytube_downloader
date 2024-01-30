from view import DownloaderApp



from controller import Controller

def main():
        
        #Create the main window
        view = DownloaderApp()
        Controller(view)
        
        view.mainloop() 
        
if __name__ == "__main__":
    main()