"""
This file manages the song downloads

"""

import os
import random

cwd = os.getcwd() #gets current working directory
temp_path = f'{os.environ["USERPROFILE"]}/AppData/Local/Temp'
rand_number = 0
user = f"""{os.environ["USERPROFILE"]}\\Music"""

def start_Download(url):

    '''Main downloading funtion'''

    global rand_number, user
    rand_number = random.random()

    with open(f"{temp_path}/MusifyTemp_{rand_number}.vbs","wt") as f:
        with open("Downloader.xfd","rt") as x: #Opens the Downloader.xfd file that is responsible for downloading the song.
            f.write(x.read().replace("cwd",cwd).replace("user", user).replace("url",url))

    os.startfile(f"{temp_path}/MusifyTemp_{rand_number}.vbs")
