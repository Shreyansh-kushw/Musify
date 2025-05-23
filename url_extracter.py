'''Program the will manage all the tasks related to extracting URL of songs to be played.'''

import subprocess
import requests

# ------------------- EXTRACT URL FUNCTION ------------------- #

def Extract(topic):
    """Will play video on following topic, takes about 10 to 15 seconds to load"""
    url = 'https://www.youtube.com/results?q=' + topic
    count = 0
    cont = ''
    try:
        cont = requests.get(url)
    except:
        print('Error','Cannot Connect.. Internet not connected or invalid URL or id.')
        cont = ''
    
    try:

        data = cont.content
        data = str(data)
        lst = data.split('"')
        for i in lst:
            count+=1
            if i == 'WEB_PAGE_TYPE_WATCH':
                break
        if lst[count-5] == "/results":
            print("Error","No video found.")
        return (("https://www.youtube.com"+lst[count-5]).split("""\\"""))[0]
    
    except:

        pass

# ------------------------------------------------------------ #

def url_extracter(song_yt_url):

    '''Find the direct song/video url for a song from youtube URL using Yt-dlp'''

    song_url = str(subprocess.check_output(f'yt-dlp.exe -q -g {Extract(song_yt_url)}')).split("\\n")
    return song_url[1] #Returns the song/audio URL

# ------------------------------------------- The END ------------------------------------------- #