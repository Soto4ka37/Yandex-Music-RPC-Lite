from yandex_music import Client
from tkinter import messagebox
import sys
from modules.data import save_settings, load_settings

def gettoken(settings: dict) -> str:
    token = settings.get('token')
    if not token or len(token) <= 3:
        try:
            from modules.token.wx import get_token
            token = get_token()
            settings['token'] = token
        except Exception as e:
            chrome_err = str(e)
        if not token or len(token) <= 3:
            try:
                from modules.token.chrome import get_token
                token = get_token()
                settings['token'] = token
                save_settings(settings)
            except Exception as e:
                err = str(e)
            if not token or len(token) <= 3:
                messagebox.showerror("Ошибка", f"Не удалось получить токен!\n\nСпособ от KysTik31: {err}\nСпособ через Google Chrome: {chrome_err}")
                sys.exit()   
    settings['token'] = token
    save_settings(settings)
    return token

def getclient() -> Client:
    settings = load_settings()
    token = gettoken(settings)
    try:
        client = Client(token)
    except:
        token = gettoken(settings)
        client = Client(token)
    return client

class API:
    def __init__(self, client: Client):
        self.client = client

    def update(self):
        try:
            queue_list = self.client.queues_list()[0]
            self.type = queue_list.context.type
            self.description = queue_list.context.description
            self.partdone = True
            try:
                queue = self.client.queue(queue_list.id)
                last_track_id = queue.get_current_track()
                last_track = last_track_id.fetch_track()
                duration = last_track.duration_ms
                duration_min = (duration // (1000 * 60)) % 60
                duration_sec = (duration // 1000) % 60
                duration_raw = duration // 1000
                album = last_track.albums

                self.type = 'track'
                self.name = last_track.title
                self.album = album[0].title
                self.count = album[0].track_count
                self.authors = ', '.join(last_track.artists_name())
                self.link = f"https://music.yandex.ru/track/{last_track['id']}/"
                self.icon = "https://" + last_track.cover_uri.replace("%%", "200x200")
                self.minutes = duration_min
                self.seconds = duration_sec
                self.total = duration_raw
                self.fulldone = True
                self.error = None
            except Exception as e:
                if str(e) not in ('Timed out', 'None', 'Bad Gateway'):
                    self.fulldone = False
                    self.name = None
                    self.album = None
                    self.count = None
                    self.authors = None
                    self.link = None
                    self.icon = None
                    self.minutes = None
                    self.seconds = None
                    self.total = None
        except:
            self.error = str(e)
            self.type = None
            self.description = None
            self.partdone = False