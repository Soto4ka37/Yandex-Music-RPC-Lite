from configparser import ConfigParser
import datetime
from modules.button import BTNget
config = ConfigParser()
config.read('info/config.ini')
from pypresence import Presence
dRPC = Presence(client_id=1116090392123822080)
dRPC.connect()

class MRPC:
    def mywave1(wavetime):
        dRPC.update(
            details='"Моя волна"',
            state='Нет информации о треке',
            large_image='mywave',
            small_image='logo',
            small_text="Yandex Music RPC Lite by Soto4ka37",
            start=wavetime,
        )
    def mywave0():
        dRPC.update(
            details='"Моя волна"',
            state='Нет информации о треке',
            large_image='mywave',
            small_image='logo',
            small_text="Yandex Music RPC Lite by Soto4ka37",
        )
    def update2(song):
        end_time = int((datetime.datetime.now() + datetime.timedelta(minutes=song[5], seconds=song[6])).timestamp())
        dRPC.update(
            details=f'{song[0]:0>2}',
            state=f'{song[1]:0>2}', 
            large_image=song[4],
            small_image='logo',
            large_text=f"{song[0]} [{song[5]}:{song[6]:0>2}]",
            small_text=f'Длинна трека: {song[5]}:{song[6]:0>2}',
            end=end_time,
            buttons=BTNget.btn(song),
        )
    def update0(song):
        dRPC.update(
            details=f'{song[0]:0>2}',
            state=f'{song[1]:0>2}', 
            large_image=song[4],
            small_image='logo',
            large_text=f"{song[0]} [{song[5]}:{song[6]:0>2}]",
            small_text=f'Длинна трека: {song[5]}:{song[6]:0>2}',
            buttons=BTNget.btn(song),
        )
    def repeat2(song, lastupdatetimestamp):
        dRPC.update(
            details=f'{song[0]:0>2}',
            state=f'{song[1]:0>2}', 
            large_image=song[4],
            small_image='repeat',
            large_text=f"{song[0]} [{song[5]}:{song[6]:0>2}]",
            small_text=f'Трек повторяется',
            buttons=BTNget.btn(song),
            start=lastupdatetimestamp,
        )
    def repeat1(song):
        end_time = int((datetime.datetime.now() + datetime.timedelta(minutes=song[5], seconds=song[6])).timestamp())
        dRPC.update(
            details=f'{song[0]:0>2}',
            state=f'{song[1]:0>2}', 
            large_image=song[4],
            small_image='repeat',
            large_text=f"{song[0]} [{song[5]}:{song[6]:0>2}]",
            small_text=f'Трек повторяется',
            end=end_time,
            buttons=BTNget.btn(song),
        )
    def repeat0(song):
        dRPC.update(
            details=f'{song[0]:0>2}',
            state=f'{song[1]:0>2}', 
            large_image=song[4],
            small_image='repeat',
            large_text=f"{song[0]} [{song[5]}:{song[6]:0>2}]",
            small_text=f'Трек повторяется',
            buttons=BTNget.btn(song),
        )