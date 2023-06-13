import os
import datetime
from configparser import ConfigParser

config = ConfigParser()
config.read('info/config.ini')
mode = config.get("settings", "mode")
import time
from modules.rpc import MRPC
from modules.yandexmusic import MYAPI
from threading import Thread
if not (mode == "0" or mode == "1" or mode == "2"):
    print('РЕЖИМ НЕ УСТАНОВЛЕН ИЛИ УСТАНОВЛЕН НЕ ПРАВИЛЬНО')
    mode = "2"
    print('Используется режим по умолчнаию')
if mode == "0": 
    print("Скрипт запущен в классическом режиме (Подробнее в папке info)")
if mode == "1":
    print('Скрипт запущен в первом режиме повтора (Подробнее в папке info)')
if mode == "2":
    print('Скрипт запущен во втором режиме повтора (Подробнее в папке info)')
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
                repeat = 0
                if mode == "1" or "2":
                    MRPC.update2(song)
                if mode == "0":
                    MRPC.update0(song)
                print(f'[RPC] Смена трека: {song[1]} - {song[0]} ({song[5]}:{song[6]:0>2})')
                lastupdate = datetime.datetime.now()
                lastupdatetimestamp = int(datetime.datetime.now().timestamp())
            if repeat == 0:
                time_repeat = (datetime.datetime.now() - lastupdate).total_seconds()
                #print(f'До перехода в режим повтора: {time_repeat}/{song[7]}')
                if time_repeat > song[7] + 3:
                    if mode == "2":
                        MRPC.repeat2(song, lastupdatetimestamp)
                        repeat = 1
                        print('[RPC] Трек не изменился, перехожу в режим повтора')
                    if mode == "1":
                        MRPC.repeat1(song)
                        print('[RPC] Трек не изменился, начинаю осчёт сначала')
                        lastupdate = datetime.datetime.now()
                    if mode == "0":
                        MRPC.repeat0(song)
                        repeat = 1
        except Exception as e:
            #print('Трек не известен. Играет "Моя волна"?')
            lasttrack = 0
            repeat = 0
            MRPC.mywavePresence()            
        time.sleep(0.01)

if __name__ == "__main__":
    t1 = Thread(target=app)
    t1.start()
    t1.join()