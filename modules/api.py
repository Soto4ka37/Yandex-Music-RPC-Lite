from yandex_music import Client, exceptions
from tkinter import messagebox
import sys
from modules.data import save_settings, settings_path, settings
import modules.debugger as debugger
#import traceback
def updateToken() -> str:
    token = settings.get('token')
    wxTokenError = None
    ChromeTokenError = None
    if not token or len(token) <= 3:
        debugger.addRequest('Запущен процесс получения токена')
        try:
            from modules.token.wx import get_token
            token = get_token()
            settings['token'] = token
            save_settings(settings)
        except Exception as e:
            wxTokenError = str(e)
        if not token or len(token) <= 3:
            try:
                from modules.token.chrome import get_token
                token = get_token()
                settings['token'] = token
                save_settings(settings)
            except Exception as e:
                ChromeTokenError = str(e)
            if not token or len(token) <= 3:
                messagebox.showerror("API Unauthorized", f"Неудачная авторизация в Yandex Music API!\n\nСпособ от KysTik31: {wxTokenError}\nСпособ через Google Chrome: {ChromeTokenError}")
                sys.exit()   

    visible_chars = 4
    prefix = token[:visible_chars]
    suffix = token[-visible_chars:]
    masked_chars = '*' * 10
    censored_token = prefix + masked_chars + suffix
    debugger.addInfo(f'Текущий токен {censored_token} хранится в {settings_path} (Никогда не передавайте ваш токен третьим лицам!)')
    return token

def getClient() -> Client:
    token = updateToken()
    try:
        client = Client(token).init()
        if not client or not client.accountStatus():
            raise exceptions.UnauthorizedError
    except Exception as e:
        debugger.addError('Неудачная авторизация!')
        settings['token'] = None
        token = updateToken()
        client = Client(token).init()
    status = client.accountStatus()
    debugger.addInfo(f'Успешная авторизация! Подписка на плюс: {status.plus.has_plus}')
    return client

class NotQueue(Exception):
    def __init__(self, message):
        super().__init__(message)

class API:
    def __init__(self, client: Client):
        self.client = client
        self.now = None
        self.fulldone = None

    def update(self):
        try:
            queue_list = self.client.queues_list()
            if queue_list:
                queue = queue_list.pop(0)
            else:
                raise NotQueue('Неудаётся получить текущую очередь. Возвращён пустой список с серверов Яндекса.')
            self.type = queue.context.type
            self.description = queue.context.description
            try:
                queue = self.client.queue(queue.id)
                last_track_id = queue.get_current_track()
                if not self.now or last_track_id.track_id != self.now.track_id:
                    self.now = last_track_id
                    last_track = last_track_id.fetch_track()
                    duration = last_track.duration_ms
                    duration_min = (duration // (1000 * 60)) % 60
                    duration_sec = (duration // 1000) % 60
                    duration_raw = duration // 1000
                    album = last_track.albums

                    self.count_tracks_in_queue = len(queue.tracks) + 1
                    self.now_track_in_queue = queue.current_index + 1
                    self.type = 'track'
                    self.name = last_track.title
                    self.album = album[0].title
                    self.album_count = album[0].track_count
                    self.authors = ', '.join(last_track.artists_name())
                    self.link = f"https://music.yandex.ru/track/{last_track.id}/"
                    self.url = f"https://music.yandex.ru/track/{last_track.id}/"
                    self.album_url = f"https://music.yandex.ru/track/{album[0].id}/"
                    self.icon = "https://" + last_track.cover_uri.replace("%%", "200x200")
                    self.minutes = duration_min
                    self.seconds = duration_sec
                    self.total = duration_raw
                    self.fulldone = True
            except Exception as e:
                #print(traceback.format_exc())
                if not isinstance(e, exceptions.TimedOutError):
                    self.fulldone = False
                    self.partdone = True
                    self.count_tracks_in_queue = '∞'
                    self.now_track_in_queue = 0
                    self.name = 'Неизвестно'
                    self.album = 'Неизвестно'
                    self.album_count = 0
                    self.authors = 'Неизвестно'
                    self.link = 'https://music.yandex.ru/'
                    self.url = 'https://music.yandex.ru/'
                    self.icon = 'https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Icon.png'
                    self.minutes = 0
                    self.seconds = 0
                    self.total = 0
                    self.now = None
                else:
                    debugger.addWarning('TimedOut: Яндекс слишком долго не отвечал на запрос.')
        except Exception as e:
            if not isinstance(e, exceptions.TimedOutError):
                debugger.addWarning('TimedOut: Яндекс слишком долго не отвечал на запрос.')
                raise e