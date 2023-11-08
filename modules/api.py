from yandex_music import Client
from modules.data import load_settings, save_settings
from tkinter import messagebox
import sys
settings = load_settings()

def get_token():
    token = settings.get('token')
    if not token or len(token) <= 3:
        try:
            from modules.token.wx import get_token
            token = get_token()
            settings['token'] = token
            save_settings(settings)
        except Exception as e:
            chrome_err = str(e)
        token = settings.get('token')
        if not token or len(token) <= 3:
            try:
                from modules.token.chrome import get_token
                token = get_token()
                settings['token'] = token
                save_settings(settings)
            except Exception as e:
                err = str(e)
            token = settings.get('token')
            if not token or len(token) <= 3:
                messagebox.showerror("Ошибка", f"Не удалось получить токен!\n\nСпособ от KysTik31: {err}\nСпособ через Google Chrome: {chrome_err}")
                sys.exit()   
            else:
                return token
        else:
            return token
    else:
        return token
        
def run():
    global client
    token = get_token()
    try:
        client = Client(token).init()
    except:
        settings['token'] == "0"
        save_settings(settings)
        token = get_token()
        client = Client(token).init()


class Radio:
    def __init__(self):
        if not client:
            raise Exception('Нет клиента, для начала выполните run()')
        self.client = client
        self.update()

    def update(self):
        try:
            queue_list = self.client.queues_list()[0]

            self.type = queue_list["context"]["type"]
            self.name = queue_list["context"]["description"]
            self.done = True
            self.error = None
        except Exception as e:
            if str(e) not in ['Timed out', 'None', 'Bad Gateway']:
                self.error = e
                self.done = False
                self.type = None
                self.name = None

class Song:
    def __init__(self):
        if not client:
            raise Exception('Нет клиента, для начала выполните run()')
        self.client = client
        self.update()

    def update(self):
        try:
            queue = self.client.queue(self.client.queues_list()[0].id)
            last_track_id = queue.get_current_track()
            last_track = last_track_id.fetch_track()
            duration = last_track.duration_ms
            duration_min = (duration // (1000 * 60)) % 60
            duration_sec = (duration // 1000) % 60
            duration_raw = duration // 1000
            album = last_track.albums

            self.type = 'track'  # Тип
            self.name = last_track.title  # Название трека
            self.album = album[0]['title']  # Название альбома
            self.count = album[0]['track_count']  # Число треков в альбоме
            self.authors = ', '.join(last_track.artists_name())  # Исполнители
            self.link = f"https://music.yandex.ru/album/{last_track['albums'][0]['id']}/track/{last_track['id']}/"  # Ссылка на трек
            self.icon = "https://" + last_track.cover_uri.replace("%%", "200x200")  # Картинка альбома
            self.minutes = duration_min  # Длина в минутах
            self.seconds = duration_sec  # Длина в секундах (Остаток от минут)
            self.total = duration_raw  # Длина в секундах
            self.done = True
            self.error = None
        except Exception as e:
            if str(e) not in ['Timed out', 'None', 'Bad Gateway']:
                self.error = e
                self.done = False
                self.type = None
                self.name = None
                self.album = None
                self.count = None
                self.authors = None
                self.link = None
                self.icon = None
                self.minutes = None
                self.seconds = None
                self.total = None