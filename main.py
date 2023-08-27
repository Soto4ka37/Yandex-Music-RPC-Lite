import datetime
from configparser import ConfigParser
import colorama
colorama.init()
try:
    config = ConfigParser()
    config.read('config.ini')
    import time
    mode = config.get("settings", "mode")
    wavemode = config.get("settings", "wavetime")
    button = config.get("settings", "button")
except:
    print(colorama.Fore.RED + "Файл config.ini не найден или повреждён! Пожалуйста переустановите скрипт по ссылке ниже" + colorama.Style.RESET_ALL)
    print("--------------")
    print("https://github.com/Soto4ka37/Yandex-Music-RPC-Lite/releases")
    print("--------------")
    input("Нажмите Enter чтобы завершить программу")

from modules.yandexmusic import MYAPI
from modules.rpc import MRPC
from threading import Thread

if mode not in ["True", "Single", "Restart"]:
    print(colorama.Fore.RED + '[Предупреждение] "mode" не правильно установлен! Использую "Single" как режим по умолчанию!' + colorama.Style.RESET_ALL)
    mode = True
elif mode == "True":
    mode = True

if wavemode not in ["True", "False"]:
    print(colorama.Fore.RED + '[Предупреждение] "wavetime" не правильно установлен! Использую "True" как режим по умолчанию!' + colorama.Style.RESET_ALL)
    wavemode = True
else:
    if wavemode == "True":
        wavemode = True
    else:
        wavemode = False
print(colorama.Fore.GREEN + f'[RPC] Загружены настройки из сonifg.ini'  + colorama.Style.RESET_ALL)

def app():
    update = None
    time_repeat = None
    lasttrack = None
    repeat = None
    wave = None
    while True:
        try:
            song = MYAPI.song()
            if song[3] != lasttrack:
                lasttrack = song[3]
                update = True
            if update:
                print(f'[RPC] Смена трека: {song[1]} - {song[0]} ({song[5]}:{song[6]:0>2})')
                if mode:
                    MRPC.update2(song)
                if not mode:
                    MRPC.update0(song)
                lastupdate = datetime.datetime.now()
                lastupdatetimestamp = int(datetime.datetime.now().timestamp())
                update = False
                repeat = False
                wave = False
            if not repeat:
                time_repeat = (datetime.datetime.now() - lastupdate).total_seconds()
                #print(f'До перехода в режим повтора: {time_repeat}/{song[7]}')
                if time_repeat > song[7] + 3:
                    if not mode:
                        MRPC.repeat0(song)
                        repeat = True
                    elif mode == "Single":
                        MRPC.repeat2(song, lastupdatetimestamp)
                        repeat = True
                        print('[RPC] Трек не изменился.')
                    elif mode == "Restart":
                        MRPC.repeat1(song)
                        print('[RPC] Трек не изменился.')
                        lastupdate = datetime.datetime.now()
        except Exception as e:
            #print(e)
            if str(e) in ["Timed out", "Bad Gateway"]:
                pass
            elif not wave:
                if wavemode:
                    wavetime = int(datetime.datetime.now().timestamp())
                    MRPC.mywave1(wavetime)     
                elif not wavemode:
                    MRPC.mywave0()     
                wave = True        
                lasttrack = None
                repeat = False
                print('[RPC] Нет информации о треке!')
        time.sleep(0.01)


if __name__ == "__main__":
    t1 = Thread(target=app)
    t1.start()
    t1.join()
