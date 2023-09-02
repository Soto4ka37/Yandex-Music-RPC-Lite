version = "v7"
import datetime
from configparser import ConfigParser
import colorama
colorama.init()
import time
import requests

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
    config.read('settings.ini', encoding='utf-8')
    config.get('sys', 'yandexmusictoken')
    try:
        debug = config.getboolean('sys', 'debug')
    except:
        debug = False
        print("[settings] Переменная debug в разделе sys неккоректно установлена.")
    ping = config.getint('sys', 'ping')
    mode = config.get('track', 'time')
    config.get('track', 'button')
    config.get('wave', 'time')
    config.get("nodata", "clear")
    config.get("nodata", "time")
    if mode not in ["False", "One", "Two"]:
        print(colorama.Fore.RED + '[settings] Переменная time в разделе track неккоректно установлена!' + colorama.Style.RESET_ALL)
        mode = "Two"
    elif mode == "False":
        mode = False
    return debug, mode, ping

try:
    debug, mode, ping = load_data()
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
if not mode:
    debug, mode, ping = load_data()
from modules.yandexmusic import MYAPI
from modules.rpc import MRPC2
from threading import Thread


print(colorama.Fore.GREEN + f'[RPC] Загружены настройки из сonifg.ini'  + colorama.Style.RESET_ALL)

def check_updates(version):
    url = f"https://api.github.com/repos/Soto4ka37/Yandex-Music-RPC-Lite/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        latest = response.json()
        latest_version = latest["tag_name"]
        if version != latest_version:
            print(colorama.Fore.YELLOW + f'[GitHub] Доступна новая версия скрипта! Используется: {version} Последняя: {latest_version}')
            print(colorama.Fore.CYAN + f'>>> https://github.com/Soto4ka37/Yandex-Music-RPC-Lite/releases/latest' + colorama.Style.RESET_ALL)
    else:
        print(colorama.Fore.YELLOW + f'[RPC] Не удалось проверить обновления.' + colorama.Style.RESET_ALL)
check_updates(version)
def app():
    update = None
    time_repeat = None
    lasttrack = None
    repeat = None
    no_info = None
    time_repeat = None
    lastradio = None
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
                no_info = False
            if not repeat:
                if mode:
                    time_repeat = (datetime.datetime.now() - lastupdate).total_seconds()
                #print(f'До перехода в режим повтора: {time_repeat}/{song[7]}')
                if time_repeat and time_repeat > song[7] + 3:
                    data = MRPC2.repeat(song=song, mode=mode, time=lastupdate)
                    if data:
                        repeat = True
                        print('[RPC] Трек не изменился.')
                    else:
                        lastupdate = datetime.datetime.now()
                        print(f'[RPC] Повтор трека: {song[1]} - {song[0]} ({song[5]}:{song[6]:0>2})')
        except Exception as e:
            if str(e) in ["Timed out", "Bad Gateway"]:
                pass
            elif not no_info:
                try:
                    description = MYAPI.radio()
                    if description == None:
                        raise Exception("Имя потока отсутствует")
                    if lastradio != description:
                        MRPC2.radio(state=description)
                        lasttrack = None
                        repeat = False
                        lastradio = description 
                        print(f'[RPC] Играет поток "{description}".')
                except:
                    MRPC2.none()
                    print("[RPC] Нет информации о треке!")
                    no_info = True
                if debug:
                    print(f"[Debug] {e}")
        time.sleep(ping)


if __name__ == "__main__":
    t1 = Thread(target=app)
    t1.start()
    t1.join()
