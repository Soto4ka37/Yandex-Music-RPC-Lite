from configparser import ConfigParser
import datetime
import time
config = ConfigParser()
config.read('info/config.ini')

from pypresence import Presence
dRPC = Presence(client_id=config.get('main', 'dsappid'))
dRPC.connect()

class MRPC:
    def mywavePresence():
        dRPC.update(
            details='Неизвестно или "Моя волна"',
            large_image="https://cdn.discordapp.com/attachments/1117022431748554782/1117022461045772379/logo.png",
            large_text="Yandex Music RPC Lite by Soto4ka37"
        )
    def repeat(song):
        dRPC.update(
            details=f'{song[0]}',
            state=f'{song[1]}', 
            large_image=song[4],
            small_image="https://cdn.discordapp.com/attachments/1117022431748554782/1117022460739584020/repeat.png",
            large_text=f"{song[0]} [{song[5]}:{song[6]:0>2}]",
            small_text=f'Повтор трека: ВКЛ',
            buttons=[{"label": "Слушать", "url": f"{song[2]}"}],
        )
    def update(song):
        end_time = int((datetime.datetime.now() + datetime.timedelta(minutes=song[5], seconds=song[6])).timestamp())
        dRPC.update(
            details=f'{song[0]}',
            state=f'{song[1]}', 
            large_image=song[4],
            small_image="https://cdn.discordapp.com/attachments/1117022431748554782/1117022461045772379/logo.png",
            large_text=f"{song[0]} [{song[5]}:{song[6]:0>2}]",
            small_text=f'Длинна трека: {song[5]}:{song[6]:0>2}',
            end=end_time,
            buttons=[{"label": "Слушать", "url": f"{song[2]}"}]
        )
        