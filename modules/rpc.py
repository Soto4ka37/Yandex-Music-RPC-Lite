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
        )
    def updatePresence(aritst, song, image_link, song_link, song_time):
        timerpc = int(time.time())
        dRPC.update(
            details=f'{song}',
            state=f'от {aritst}', 
            large_image=image_link,
            small_image="https://github.com/maj0roff/YandexMusicDiscordRPC/blob/main/logo.png?raw=true",
            small_text=f"Длинна: {song_time}",
            start=timerpc
        )
