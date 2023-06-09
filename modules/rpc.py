from configparser import ConfigParser
from pypresence import Presence

config = ConfigParser()

config.read('info/config.ini')

dRPC = Presence(client_id=config.get('main', 'dsappid'))
dRPC.connect()
import time

class MRPC:
    def mywavePresence():
        dRPC.update(
            details='Неизвестно или "Моя волна"',
            large_image="https://github.com/maj0roff/YandexMusicDiscordRPC/blob/main/logo.png?raw=true",
            large_text="Yandex Music RPC Lite by Soto4ka37"
        )
    def updatePresence(song):
        start_time = int(time.time())
        dRPC.update(
            details=f'{song[0]}',
            state=f'{song[1]}', 
            large_image=song[4],
            small_image="https://github.com/maj0roff/YandexMusicDiscordRPC/blob/main/logo.png?raw=true",
            large_text=f"{song[0]} [{song[5]}]",
            small_text=f'Длинна трека: {song[5]}',
            start=start_time,
            buttons=[{"label": "Слушать", "url": f"{song[2]}"}]
        )
