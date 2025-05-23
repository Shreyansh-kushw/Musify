"""
Plays the requested song without a console output
"""

# Importing some modules

import requests
import os
import ctypes

# Get the absolute path to the current script (in the subfolder)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go one level up to the main/root folder
root_dir = os.path.dirname(current_dir)

# Define VLC path assuming it's directly in the root folder
vlc_path = root_dir  

# Add to system path at runtime
os.environ["PATH"] = vlc_path + os.pathsep + os.environ["PATH"]

# Load the DLL manually. This was done to avoid the error Libvlc.dll not found.
ctypes.CDLL(os.path.join(vlc_path, "libvlc.dll"))

# import VLC
import vlc

# Configuring Yt-dlp

from yt_dlp import YoutubeDL

def get_best_audio_url(song_name):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'default_search': 'ytsearch',
        'noplaylist': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(song_name, download=False)
        # If it's a search result, extract the first entry
        if 'entries' in info:
            info = info['entries'][0]
        return info['url']



# Creating some variables

player = ""
val = ""
song_names = []
currently_playing = ""
paused = False

# --------------------- All the main Functions ---------------------#


# ========= All the webscraping funtions ===== #

def get_song_url(topic):

    """
    Function to find YouTube video URL of the Song requested....
    """

    url = 'https://www.youtube.com/results?q=' + topic + " song lyrics"
    # print(url)
    count = 0
    cont = requests.get(url)
    data = cont.content
    data = str(data)
    lst = data.split('"')
    for i in lst:
        count += 1
        if i == 'WEB_PAGE_TYPE_WATCH':
            break
    if lst[count - 5] == "/results":
        raise Exception("No video found.")

    return "https://www.youtube.com" + lst[count - 5]


def url_extracter(song_name):
    '''
    Function to find the song url.
    '''
    global currently_playing, video, song_url

    currently_playing = song_name

    video = get_best_audio_url(song_name)
    song_names.append(song_name)
    song_url = video
    
    return song_url

# ========= All the functions that play the song ===== #
def play_by_song_url(url):
    global player, val

    """
    Function to play song from video/song URL....
    """
    try:
       player.stop() #stops the player if already playing
    except:
        pass
    
    player = vlc.MediaPlayer(url)  

    player.play() #plays the song
    
def play_by_yt_url(yt_url):
    
    # Function to play song from youtube video URL

    
    play_by_song_url(url_extracter(yt_url)) #extracts the song url from the youtube url and feeds to play_by_song_url function
    # print(play_by_song_url(url_extracter(yt_url)))


def play_by_songName(song_name):

    """
    Function which will take song name as argument and then find the YouTube video url of that song;
    After that it find the video URL of the Song then play it.....
    """

    url_of_song = get_song_url(song_name)
    url_of_song = url_of_song.split("""\\""")[0]
    play_by_yt_url(url_of_song)
 
def play_by_file(file_path): #Can play a song/audio from a file path
    play_by_song_url(file_path)

# ========= All the pause, resume, rewind etc type of functions ===== #

def pause_song(): 
    '''
    Function to pause or resume the playing song.
    '''

    global player, paused
    if player != "":
        player.pause()


def next_():
    '''Plays the next song in queue'''
    pass

def previous():
    '''Plays the previous song in queue'''
    seek(0.0)



def seek(pos):
    '''Seeks the player to a specific position'''
  
    # here in the arguments we are supposed to give the seconds to which we have to seek. lIKE IF WE HAVE TO SEEK TO 20 SECONDS THEN WE HAVE TO GIVE 20 IN THE ARGUMENTS
    
    global player
    player.set_position(pos)
# ---------------------------------------------------------------------------#
