from configparser import ConfigParser
import datetime
config = ConfigParser()
config.read('info/config.ini')

from pypresence import Presence
dRPC = Presence(client_id=config.get('main', 'dsappid'))
dRPC.connect()
class MRPC:
    def mywavePresence():
        dRPC.update(
            details='Неизвестно или "Моя волна"',
            large_image='logo',
            large_text="Yandex Music RPC Lite by Soto4ka37"
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
            buttons=[{"label": "Слушать", "url": f"{song[2]}"}]
        )
    def repeat2(song):
        repeat_time = int(datetime.datetime.now().timestamp())
        dRPC.update(
            details=f'{song[0]:0>2}',
            state=f'{song[1]:0>2}', 
            large_image=song[4],
            small_image='repeat',
            large_text=f"{song[0]} [{song[5]}:{song[6]:0>2}]",
            small_text=f'Трек повторяется',
            buttons=[{"label": "Слушать", "url": f"{song[2]}"}],
            start=repeat_time,
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
            buttons=[{"label": "Слушать", "url": f"{song[2]}"}]
        )
    def update0(song):
        dRPC.update(
            details=f'{song[0]:0>2}',
            state=f'{song[1]:0>2}', 
            large_image=song[4],
            small_image='logo',
            large_text=f"{song[0]} [{song[5]}:{song[6]:0>2}]",
            small_text=f'Длинна трека: {song[5]}:{song[6]:0>2}',
            buttons=[{"label": "Слушать", "url": f"{song[2]}"}]
        )
    def repeat0(song):
        dRPC.update(
            details=f'{song[0]:0>2}',
            state=f'{song[1]:0>2}', 
            large_image=song[4],
            small_image='repeat',
            large_text=f"{song[0]} [{song[5]}:{song[6]:0>2}]",
            small_text=f'Трек повторяется',
            buttons=[{"label": "Слушать", "url": f"{song[2]}"}],
        )