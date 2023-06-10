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

lasttrack = 0
lastupdate = datetime.datetime.now()

def app():
    switch = 0
    time_repeat = 0
    lasttrack = 0
    repeat = 0
    while True:
        try:
            song = MYAPI.song()
            if song[3] != lasttrack:
                lasttrack = song[3]
                switch = 1
            if switch == 1:
                switch = 0
                afk = 0
                MRPC.update(song)
                print(f'[RPC] Смена трека: {song[1]} - {song[0]} ({song[5]}:{song[6]:0>2})')
                lastupdate = datetime.datetime.now()
            else:
                time_repeat = (datetime.datetime.now() - lastupdate).total_seconds()
                #print(f'RepeatMode: {time_repeat}/{song[7]}')
                if time_repeat > song[7] and repeat == 0:
                    MRPC.repeat(song)
                    repeat = 1
                    print('[RPC] Переключено в режим "Повтор трека" до последующей смены трека')

        except Exception as e:
            MRPC.mywavePresence()            
        time.sleep(1)

if __name__ == "__main__":
    t1 = Thread(target=app)
    t1.start()
    t1.join()