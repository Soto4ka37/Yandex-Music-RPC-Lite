from configparser import ConfigParser
import datetime
config = ConfigParser()
config.read('settings.ini', encoding='utf-8')
from pypresence import Presence
dRPC = Presence(client_id=1116090392123822080)
dRPC.connect()
button = config.getboolean("track", "button")
wavetime = config.getboolean("wave", "wavetime")

detailswave = config.get('wave', 'details')
statewave = config.get('wave', 'state')
ltwave = config.get('wave', 'large_image_text')
stwave = config.get('wave', 'icon_text')

class MRPC2:
    def button(song, setting):
        if setting:
            button = [{"label": "Слушать", "url": f"{song[2]}"}]
        else:
            button = None
        return button
    
    def wave():
        start = None
        if wavetime:
            start = int((datetime.datetime.now()).timestamp())
        dRPC.update(
            details=detailswave,
            state=statewave,
            large_image='mywave',
            small_image='logo',
            small_text=stwave,
            large_text=ltwave,
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
        if mode == 'Single':
            start = int(time.timestamp())
        elif mode == 'Restart':
            end = int((datetime.datetime.now() + datetime.timedelta(minutes=song[5], seconds=song[6])).timestamp())
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