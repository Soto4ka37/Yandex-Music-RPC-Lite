import os
import datetime
from configparser import ConfigParser

config = ConfigParser()
config.read('info/config.ini')
if len(config.get("main","yandexmusictoken")) <= 2:
    print("[RPC] Установка необходимых пакетов.")
    os.system('pip install yandex-music --upgrade')
    os.system('pip install selenium')
    os.system('pip install pypresence')
    os.system('pip install yandex_music')
    os.system('pip install webdriver_manager')
    os.system('pip install keyboard')
    os.system('pip install pywin32')
    os.system('pip install pypiwin32')

import time
from modules.rpc import MRPC
from modules.yandexmusic import MYAPI
from threading import Thread

def app():
    switch = 0
    lasttrack = 0
    while True:
        try:
            songid = MYAPI.songID()
            artist = MYAPI.songArtist()
            song = MYAPI.songTitle()
            image_link = MYAPI.songImage()
            song_link = MYAPI.songLink()
            song_time = MYAPI.songTime()
            if songid != lasttrack:
                lasttrack = songid
                switch = 1
            if switch == 1:
                switch = 0
                now_time = datetime.datetime.now()
                print(f'[RPC] [{now_time.strftime("%d.%m.%Y %H:%M:%S")}] {artist} - {song}')
                MRPC.updatePresence(artist, song, image_link, song_link, song_time)
        except Exception as e:
            now_time = datetime.datetime.now()
            #print(f'[RPC] [{now_time.strftime("%d.%m.%Y %H:%M:%S")}] Неизвестно')
            MRPC.mywavePresence()            
        time.sleep(0.1)

if __name__ == "__main__":
    t1 = Thread(target=app)
    t1.start()
    t1.join()
