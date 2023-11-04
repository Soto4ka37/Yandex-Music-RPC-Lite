try:
    import datetime
    from configparser import ConfigParser
    import colorama
    colorama.init()
    print('Вы используете устаревшую Legacy версию скрипта! Поддержка этой версии завершена 03.11.2023 \n' * 5)
    import time
    import requests
    from threading import Thread

    def load_data():
        from modules.yandexmusic import MYAPI
        from modules.rpc import MRPC2
        config = ConfigParser()
        config.read('settings.ini', encoding='utf-8')
        config.get('sys', 'yandexmusictoken')
        try:
            debug = config.getboolean('sys', 'debug')
        except:
            debug = False
            print("[settings] Переменная debug в разделе sys неккоректно установлена.")
        try:
            ping = config.getint('sys', 'ping')
        except:
            ping = 1
            print("[settings] Переменная ping в разделе sys неккоректно установлена.")
        mode = config.get('track', 'time')
        config.get('track', 'button')
        config.get('wave', 'time')
        config.get("nodata", "clear")
        config.get("nodata", "time")
        if mode not in ["False", "One", "Two"]:
            print('[settings] Переменная time в разделе track неккоректно установлена.')
            mode = "Two"
        elif mode == "False":
            mode = False
        print(colorama.Fore.GREEN + f'[RPC] Загружены настройки из settings.ini'  + colorama.Style.RESET_ALL)
        return debug, mode, ping, MYAPI, MRPC2
    
    try:
        debug, mode, ping, MYAPI, MRPC2 = load_data()
    except Exception as e:
        print(colorama.Fore.RED + 'Файл настроек settings.ini не найден или повреждён!' + colorama.Style.RESET_ALL)
        input('Нажмите Enter чтобы скачать необходимый файл в корневую папку.')
        response = requests.get("https://raw.githubusercontent.com/soto4ka37/yandex-music-rpc-lite/master/settings.ini")
        with open("settings.ini", "wb") as file:
            try:
                file.write(response.content)
                print(colorama.Fore.GREEN + "Файл settings.ini успешно скачан!" + colorama.Style.RESET_ALL)
            except:
                input(colorama.Fore.Red + "Не удалось поместить файл в корневую папку!" + colorama.Style.RESET_ALL)
        debug, mode, ping, MYAPI, MRPC2 = load_data()

    def app():
        lasttrack = None
        lastradio = None
        nowplaymode = None
        radio = False
        while True:
            song = None
            radio = None
            err = None
            try:
                try:
                    song = MYAPI.song()
                except Exception as error:
                    err = error
                    if str(error) in ["Timed out", "Bad Gateway"]:
                        continue
                    radio_data = MYAPI.radio()
                    if radio_data[1] == "radio":
                        radio = radio_data[0]
                if song:
                    if song[3] != lasttrack:
                        lasttrack = song[3]
                        nowplaymode = None
                    if nowplaymode not in ["Track", "Repeat"]:
                        print(f'[RPC] Смена трека: {song[1]} - {song[0]} ({song[5]}:{song[6]:0>2})')
                        MRPC2.update(song=song, mode=mode)
                        lastupdate = datetime.datetime.now()
                        nowplaymode = "Track"
                    elif mode and nowplaymode == "Track":
                        repeat = (datetime.datetime.now() - lastupdate).total_seconds()
                        if repeat >= song[7]:
                            MRPC2.repeat(song=song, mode=mode, time=lastupdate)
                            if mode == "One":
                                lastupdate = datetime.datetime.now()
                                print(f'[RPC] Повтор трека: {song[1]} - {song[0]} ({song[5]}:{song[6]:0>2})')
                            elif mode == "Two":
                                nowplaymode = "Repeat"
                                print('[RPC] Трек не изменился.')
                elif radio:
                    if radio != lastradio:
                        lastradio = radio
                        nowplaymode = None
                        if nowplaymode != "Radio":
                            MRPC2.radio(state=radio)
                            nowplaymode = "Radio"
                            print(f'[RPC] Играет поток "{radio}"')
                else:
                    if nowplaymode != "None":
                        MRPC2.none()
                        nowplaymode = "None"
                        print(f"[RPC] Нет данных о треке!")
                        if debug:
                            print(f'[Debug] {err}')
                            if radio_data:
                                print(f"[Debug] {radio_data[2]}")
            
            except Exception as e:
                print(colorama.Fore.RED + f"Произошла ошибка: {e}" + colorama.Style.RESET_ALL)
            time.sleep(ping)


    if __name__ == "__main__":
        t1 = Thread(target=app)
        t1.start()
        t1.join()
except Exception as e:
    import colorama
    colorama.init()
    print(colorama.Fore.RED + "Произошла критичиская ошибка при работе скрипта:" + colorama.Style.RESET_ALL)
    print(e)
    input(colorama.Fore.YELLOW + "Нажмите Enter чтобы завершить работу скрипта.")