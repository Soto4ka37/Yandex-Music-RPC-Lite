import datetime
from configparser import ConfigParser

config = ConfigParser()
config.read('info/config.ini')
import time
mode = config.get("settings", "maintime")
wavemode = config.get("settings", "wavetime")
button = config.get("settings", "button")
if not (button == "0" or button == "1"):
    print('[Ошибка] Установлен режим по умолчанию (button = 1) для этой сессии, укажите правильный режим в info/conifg.ini')
if not (mode == "0" or mode == "1" or mode == "2"):
    mode = "2"
    print('[Ошибка] Установлен режим по умолчанию (timemode = 2) для этой сессии, укажите правильный режим в info/conifg.ini')
if not (wavemode == "0" or wavemode == "1"):
    wavemode = "1"
    print('[Ошибка] Установлен режим по умолчанию (wavemode = 1) для этой сессии, укажите правильный режим в info/conifg.ini')
from modules.rpc import MRPC
from modules.yandexmusic import MYAPI
from threading import Thread
print(f'[RPC] Загружены настройки из info/conifg.ini')
def app():
    update = 0
    time_repeat = 0
    lasttrack = 0
    repeat = 0
    wave = 0
    while True:
        try:
            song = MYAPI.song()
            if song[3] != lasttrack:
                lasttrack = song[3]
                update = 1
            if update == 1:
                update = 0
                repeat = 0
                wave = 0
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
                    elif mode == "1":
                        MRPC.repeat1(song)
                        print('[RPC] Трек не изменился, начинаю осчёт сначала')
                        lastupdate = datetime.datetime.now()
                    elif mode == "0":
                        MRPC.repeat0(song)
                        repeat = 1
        except Exception as e:
            if str(e) == "Timed out":
                pass
            elif wave == 0 and wavemode == "1":
                print(e)
                print('[RPC] Нет информации о треке. Возможно у вас включен поток')
                lasttrack = 0
                repeat = 0
                wavetime = int(datetime.datetime.now().timestamp())
                MRPC.mywave1(wavetime)     
                wave = 1
            elif wave == 0 and wavemode == "0":
                print('[RPC] Нет информации о треке. Возможно у вас включен поток')
                lasttrack = 0
                repeat = 0
                MRPC.mywave0()     
                wave = 1            
        time.sleep(0.01)


if __name__ == "__main__":
    t1 = Thread(target=app)
    t1.start()
    t1.join()
