from configparser import ConfigParser
import datetime
import colorama
colorama.init()
config = ConfigParser()
config.read('settings.ini', encoding='utf-8')
from pypresence import Presence
dRPC = Presence(client_id=1116090392123822080)
dRPC.connect()

try:
    button = config.getboolean("track", "button")
except:
    button = True
    print("[settings] Переменная button в разделе track неккоректно установлена.")
try:
    wavetime = config.getboolean("wave", "time")
except:
    wavetime = True
    print("[settings] Переменная time в разделе wave неккоректно установлена.")
try:
    noneclear = config.getboolean("nodata", "clear")
except:
    noneclear = False
    print("[settings] Переменная clear в разделе nodata неккоректно установлена.")
if noneclear:
    try:
        nonetime = config.getboolean("nodata", "time")
    except:
        nonetime = True
        print("[settings] Переменная time в разделе nodata неккоректно установлена.")
else:
    nonetime = None

class MRPC2:
    def button(song, setting):
        if setting:
            button = [{"label": "Слушать", "url": f"{song[2]}"}]
        else:
            button = None
        return button
    def none():
        time = None
        if noneclear:
            dRPC.clear()
        elif nonetime:
            time = int(datetime.datetime.now().timestamp())
        if not noneclear:
            dRPC.update(
                details="Нет данных о треке",
                state="Неизвестно",
                large_image='logo',
                large_text="Нет данных",
                start=time
            )
    def radio(state):
        start = None
        if wavetime:
            start = int((datetime.datetime.now()).timestamp())
        dRPC.update(
            details="Слушает радио",
            state=f'"{state}"',
            large_image='mywave',
            small_image='logo',
            start=start,
        )
    def update(song, mode):
        end_time = None
        if mode:
            end_time = int((datetime.datetime.now() + datetime.timedelta(minutes=song[5], seconds=song[6])).timestamp())
        dRPC.update(
            details=f'{song[0]:0>2}',
            state=f'{song[1]:0>2}', 
            large_image=song[4],
            small_image='logo',
            large_text=f"{song[8]} ({song[9]} треков)",
            small_text=f'Длинна трека: {song[5]}:{song[6]:0>2}',
            end=end_time,
            buttons=MRPC2.button(song, button),
        )
    def repeat(song, mode, time):
        start = None
        end = None
        if mode == 'Two':
            start = int(time.timestamp())
            data = True
        elif mode == 'One':
            end = int((datetime.datetime.now() + datetime.timedelta(minutes=song[5], seconds=song[6])).timestamp())
            data = False
        dRPC.update(
            details=f'{song[0]:0>2}',
            state=f'{song[1]:0>2}', 
            large_image=song[4],
            small_image='repeat',
            large_text=f"{song[8]} ({song[9]} треков)",
            small_text=f'Трек повторяется',
            buttons=MRPC2.button(song, button),
            end=end,
            start=start,
        )   
        return data