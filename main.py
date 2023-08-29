version = "v6"
import datetime
from configparser import ConfigParser
import colorama
import time
import requests

colorama.init()
def check_updates(version):
    url = f"https://api.github.com/repos/Soto4ka37/Yandex-Music-RPC-Lite/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        latest = response.json()
        latest_version = latest["tag_name"]
        if version != latest_version:
            print(colorama.Fore.YELLOW + f'[GitHub] Вышла новая версия скрипта! Используется: {version}. Последняя: {latest_version}')
            print(f'>>> https://github.com/Soto4ka37/Yandex-Music-RPC-Lite/releases/latest' + colorama.Style.RESET_ALL)
    else:
        print(colorama.Fore.YELLOW + f'[RPC] Не удалось проверить обновления.' + colorama.Style.RESET_ALL)
def load_data():
    config = ConfigParser()
    global debug, mode, ping
    config.read('settings.ini', encoding='utf-8')
    yandexmusictoken = config.get('sys', 'yandexmusictoken')
    debug = config.getboolean('sys', 'debug')
    ping = config.getint('sys', 'ping')
    mode = config.get('track', 'mode')
    button = config.getboolean('track', 'button')
    wavetime = config.getboolean('wave', 'wavetime')
    details = config.get('wave', 'details')
    state = config.get('wave', 'state')
    large_image_text = config.get('wave', 'large_image_text')
    icon_text = config.get('wave', 'icon_text')
try:
    load_data()
except Exception as e:
    print(colorama.Fore.RED + 'Файл настроек settings.ini не найден или повреждён!' + colorama.Style.RESET_ALL)
    input(colorama.Fore.GREEN + 'Нажмите Enter чтобы скачать необходимый файл в корневую папку.' + colorama.Style.RESET_ALL)
    response = requests.get("https://raw.githubusercontent.com/soto4ka37/yandex-music-rpc-lite/master/settings.ini")
    with open("settings.ini", "wb") as file:
        try:
            file.write(response.content)
            print(colorama.Fore.GREEN + "Файл settings.ini успешно скачан!" + colorama.Style.RESET_ALL)
            time.sleep(1)
        except:
            input(colorama.Fore.Red + "Не удалось поместить файл в корневую папку!" + colorama.Style.RESET_ALL)
load_data()
from modules.yandexmusic import MYAPI
from modules.rpc import MRPC2
from threading import Thread

if mode not in ["False", "Single", "Restart"]:
    print(colorama.Fore.RED + '[Предупреждение] "mode" не правильно установлен! Использую "Single" как режим по умолчанию!' + colorama.Style.RESET_ALL)
    mode = "Single"
elif mode == "False":
    mode = False

print(colorama.Fore.GREEN + f'[RPC] Загружены настройки из сonifg.ini'  + colorama.Style.RESET_ALL)

def check_updates(version):
    url = f"https://api.github.com/repos/Soto4ka37/Yandex-Music-RPC-Lite/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        latest = response.json()
        latest_version = latest["tag_name"]
        if version != latest_version:
            print(colorama.Fore.YELLOW + f'[GitHub] Доступна новая версия скрипта! Используется: {version}. Последняя: {latest_version}')
            print(f'>>> https://github.com/Soto4ka37/Yandex-Music-RPC-Lite/releases/latest' + colorama.Style.RESET_ALL)
    else:
        print(colorama.Fore.YELLOW + f'[RPC] Не удалось проверить обновления.' + colorama.Style.RESET_ALL)
check_updates(version)
def app():
    update = None
    time_repeat = None
    lasttrack = None
    repeat = None
    wave = None
    time_repeat = None
    while True:
        try:
            song = MYAPI.song()
            if song[3] != lasttrack:
                lasttrack = song[3]
                update = True
            if update:
                print(f'[RPC] Смена трека: {song[1]} - {song[0]} ({song[5]}:{song[6]:0>2})')
                MRPC2.update(song=song, mode=mode)
                lastupdate = datetime.datetime.now()
                update = False
                repeat = False
                wave = False
            if not repeat:
                if mode:
                    time_repeat = (datetime.datetime.now() - lastupdate).total_seconds()
                #print(f'До перехода в режим повтора: {time_repeat}/{song[7]}')
                if time_repeat and time_repeat > song[7] + 3:
                    MRPC2.repeat(song=song, mode=mode, time=lastupdate)
                    if mode == "Single":
                        repeat = True
                        print('[RPC] Трек не изменился.')
                    else:
                        lastupdate = datetime.datetime.now()
                        print(f'[RPC] Повтор трека: {song[1]} - {song[0]} ({song[5]}:{song[6]:0>2})')
        except Exception as e:
            if str(e) in ["Timed out", "Bad Gateway"]:
                pass
            elif not wave:
                MRPC2.wave()
                wave = True        
                lasttrack = None
                repeat = False
                print('[RPC] Нет информации о треке!')
                if debug:
                    print(f"[Debug] {e}")
        time.sleep(ping)


if __name__ == "__main__":
    t1 = Thread(target=app)
    t1.start()
    t1.join()
