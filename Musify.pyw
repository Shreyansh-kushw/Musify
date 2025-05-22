
# About Author

__author__ = "Shreyansh Kushwaha"
__license__ = "GPL"
__version__ = "3.2.0"

# Importing required libraries and files

from tkinter import *
import os
from threading import *
from PIL import ImageTk
import Play_DLL
import Dwl_Manager
import url_extracter
import customtkinter
import yt_dlp
from time import sleep
import time

class Musify():

    def __init__(self):
        # -------------------  Basic Variable Setup -------------------  #

        self.music_dir = f"""{os.environ["USERPROFILE"]}\\Music"""
        self.images_dir = f"""{os.getcwd()}\\Images"""
        self.queue = []
        self.song_duration = 0
        self.song_url = ""
        self.currently_playing = ""
        self.SongName = ""
        self.paused = False
        self.close_app  = False
        self.length = 0

    def close_code(self):

        """ Function to close the app """

        global close_app

        print("entered")

        close_app = True
        try:
            Play_DLL.player.stop()
        except:
            pass
        self.window.destroy()

        exit()
    
    
    #creating functions that will add the temporary text in the search box
    
    def on_entry_click(self, event):
        """function that gets called whenever entry is clicked"""
        if self.token_entry.get() == 'Search':
            self.token_entry.delete(0, "end") # delete all the text in the entry
            self.token_entry.insert(0, '') #Insert blank for user input

    def on_focusout(self,event):
        """function that gets called whenever entry is out of focus"""
        if self.token_entry.get() == '':
            self.token_entry.insert(0, 'Search')
    
    def downloader(self):
        """ 
        Function to start a new thread that will download the song        
        """
        t1=Thread(target=self.start_download)
        t1.start()
    
    def start_download(self):  
        
        """ Function to download the song """

        print("started")
        Dwl_Manager.start_Download(f'''{url_extracter.Extract(self.token_entry.get()+"song lyrics")}''')
    
    def add_to_queue(self, song_name):

        """ Function to add the name of the songs to the queue."""

        self.queue.append(song_name)
    
    def song_player(self):

        """ Starts a new thread that will play the song """

        self.play_thread=Thread(target=self.input_manager)
        self.play_thread.start()
    
    def progress_manager(self):

        """ Starts a new thread that will manage the progress bar. """

        self.progress_thread = Thread(target=self.ProgressBar)
        self.progress_thread.start()

    def pause_resumer(self):
        
        """ Function that will pause/resume the song. """
        if Play_DLL.player != "":
            if Play_DLL.paused:
                Play_DLL.paused = False
                self.play_photo = PhotoImage(file = f"{self.images_dir}/paused.png")
                print("resumed")
            else:
                Play_DLL.paused = True
                self.play_photo = PhotoImage(file = f"{self.images_dir}/playing.png")
                
                print("paused")
        
        else:
            pass
        
        self.play_button.configure(image=self.play_photo)

        pause_thread = Thread(target=Play_DLL.pause_song)
        pause_thread.start()

    def set_song_name_label(self, song_name):
        
        """ 
        Function that will create a Label widget to display the song name 
        """

        self.SongNameLabel.configure(text = f"{song_name}")

    def rewind(self):
            
        """ Function that will rewind the song by 10 seconds """

        print("-10s")
        print(Play_DLL.player.get_time())

        if Play_DLL.player.get_time() > 10000:
            Play_DLL.player.set_time(Play_DLL.player.get_time() - 10000)
            self.i = self.i - 10
        
        else:
            Play_DLL.seek(0)
            self.i = 0
        
        

    def forward(self):
            
        """ Function that will forward the song by 10 seconds """

        print(Play_DLL.player.get_time())

        Play_DLL.player.set_time(Play_DLL.player.get_time() + 10000)
        self.i = self.i + 10

    def get_clean_song_name(self, url):
        self.ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'nocheckcertificate': True,
            'forcejson': True,
            'extract_flat': True,
        }
    
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            self.info = ydl.extract_info(url, download=False)

        # Extract metadata
        self.track = self.info.get('track')
        self.artist = self.info.get('artist')
        self.title = self.info.get('title')

        if self.track and self.artist:
            self.clean_name = f"{self.track} - {self.artist}"
        else:
            # Fallback to raw title if metadata is missing
            self.clean_name = self.title

        return self.clean_name

    def input_manager(self):

        """
        Function that will manage all the user input.
        """
        print(url_extracter.Extract(self.token_entry.get()+ "song lyrics"))
        self.url=url_extracter.Extract(self.token_entry.get() + " official")
        self.SongName = yt_dlp.YoutubeDL({'quiet': True}).extract_info(url_extracter.Extract(self.token_entry.get() + " song lyrics"), download=False)['title']
        self.currently_playing = self.token_entry.get()+" song lyrics"
        self.current_song = self.currently_playing

        
        print(self.SongName)
        
        self.SongNameLabel["text"] = self.get_clean_song_name(self.url)
        self.add_to_queue(self.currently_playing)

        self.slider.set(0)
        Play_DLL.play_by_songName(self.currently_playing)
        
        self.progress_manager()

    def ProgressBar(self):
    
        """ Function that will manage the progress bar position"""

        self.length = yt_dlp.YoutubeDL({'quiet': True}).extract_info(url_extracter.Extract(self.token_entry.get()), download=False)['duration']

        x = self.length
        self.i = 0

        while self.i <= x:
            if not self.paused:

                try:

                    print(Play_DLL.player.get_position())
                    print(self.length*Play_DLL.player.get_position())
                    self.slider.set(Play_DLL.player.get_position())
                    
                except:
                    pass
            
                self.i += 1

            if self.close_app:
                try:
                    Play_DLL.player.stop()

                except:
                    exit()
                exit()
                    
                # print(i)
            sleep(1)
            
        else:
            while self.paused:

                for x in range(1):
                    sleep(1)

                if self.close_app:
                    Play_DLL.player.stop()
                    exit()

        self.slider.set(1) # Sets the progress bar position when the song is over
        self.SongNameLabel["text"] = ""
        time.sleep(1)
        self.slider.set(0)


    def run(self):

        # -------------------  Basic GUI Setup -------------------  #

        self.window = customtkinter.CTk()
        self.window.title("Musify")
        self.window.iconbitmap(f"{self.images_dir}/icon.ico")
        self.window.configure(bg = "#25242C")
        self.window.resizable(False, False) 
        self.window.protocol('WM_DELETE_WINDOW', self.close_code) # overriding the function of the X button in the title bar

        # Set the geometry of Tkinter Frame
        self.window.geometry("1095x600")

        # Create a Canvas
        canvas = customtkinter.CTkCanvas(
            self.window, 
            width=700, 
            height=3500,
            bg = "#FFFFFF",
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
            )
        canvas.pack(fill=BOTH, expand=True)

        # creating  the Image File
        self.bg = ImageTk.PhotoImage(file=f"{os.getcwd()}/Images/background.jpg")

        # Add Image inside the Canvas
        canvas.create_image(0, 0, image = self.bg, anchor='nw')

        # creating a search box widget
        self.token_entry = Entry(
            bd = 0,
            bg = "#25242C", 
            highlightthickness = 0, 
            font=('callibri 20')
            )

        # Inserting the temporary Search text in the search box
        self.token_entry.insert(0, "Search")
        self.token_entry.config(fg = '#DCCAFC')
        self.token_entry.config(insertbackground = '#DCCAFC')

        # packing that widget in the tkinter windows
        self.token_entry.place(
            x = 225, 
            y = 218,
            width = 600.0,
            height = 30
            )

        #configuring the search box to add the functions
        self.token_entry.bind('<FocusIn>', self.on_entry_click)
        self.token_entry.bind('<FocusOut>', self.on_focusout)


        # Loading the image files

        self.play_photo     = PhotoImage(file = f"{self.images_dir}/paused.png")
        self.download_photo = PhotoImage(file = f"{self.images_dir}/download.png")
        self.search_photo   = PhotoImage(file = f"{self.images_dir}/search.png")
        self.rewind_image   = PhotoImage(file = f"{self.images_dir}/rewind_10s.png")
        self.forward_image  = PhotoImage(file = f"{self.images_dir}/forward_10s.png")
    
        # Creating additional widgets

        self.SongNameLabel = Label(
            text=self.SongName, 
            background="#25242C", 
            foreground="white",
            font=("Aerial", 20)
            )
        

        self.play_button= Button(
            self.window, 
            image=self.play_photo,
            borderwidth=0, 
            border=0, 
            relief="flat",
            command=self.pause_resumer,
            width=50, 
            height=50
            )    

        self.slider = customtkinter.CTkSlider(
            master = self.window,  
            bg_color="#25242D", 
            width=600, 
            progress_color = "#DCCAFC"
            )
            
        self.slider.set(0)
       

        download_button= Button(
            self.window, 
            image=self.download_photo,
            borderwidth=0, 
            border=0, 
            command= self.downloader,
            width=38, 
            height=37
            )

        search_button= Button(
            self.window, 
            image=self.search_photo,
            borderwidth=0,
            border=0, 
            command= self.song_player,
            width= 38, 
            height=37
            )

        rewind_button= Button(
            self.window, 
            image=self.rewind_image,
            borderwidth=0, 
            border=0, 
            command= self.rewind,
            width= 50, 
            height=50
            )

        forward_button = Button(
            self.window, 
            image=self.forward_image,
            borderwidth=0, 
            border=0, 
            command= self.forward,
            width= 50, 
            height=50
            )

        # Packing the widgets in the tkinter window

        canvas.create_window(547, 300, window=self.SongNameLabel)
        canvas.create_window(547, 350, window=self.slider)
        canvas.create_window(547, 420, window=self.play_button)
        canvas.create_window(920, 234, window=download_button)
        canvas.create_window(857, 234, window=search_button)
        canvas.create_window(647, 420, window=forward_button)
        canvas.create_window(447, 420, window=rewind_button)

        self.window.mainloop()

App = Musify()
App.run()
