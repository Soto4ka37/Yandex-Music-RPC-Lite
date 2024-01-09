from time import time
from pypresence import Presence
from modules.api import API
import modules.debugger as debugger
import traceback
from modules.data import settings

class RPC:
    def __init__(self):
            try:
                self.rpc = Presence(client_id=1116090392123822080)
                self.rpc.connect()
                self.exception = None
                self.success = True
                debugger.addRequest('Подключено к дискорду')
            except Exception as e:
                self.exception = str(type(e).__name__)
                self.success = False
                debugger.addError(f'Неудачная попытка подключения к дискорду. \n{traceback.format_exc()}')

    def __button(self, song: API, mode: str):
        t_button = settings.get('t_button', True)

        buttons = []
        if t_button:
            for i in range(1, 3):
                key = f'b{i}_{mode}'
                if t_button and settings.get(key):
                    label_key = f'first_button_label' if i == 1 else f'second_button_label'
                    url_key = f'first_button_url' if i == 1 else f'second_button_url'

                    label = self.param_to_text(settings.get(label_key, ''), song)
                    url = self.param_to_text(settings.get(url_key, ''), song)

                    if label and url:
                        buttons.append({"label": label, "url": url})

        return buttons if buttons else None

    def param_to_text(self, text: str, song: API) -> str:
        if self.check_text_in_str(text) == None:
            return None

        def edit(text: str, check: str, param: str):
            if param:
                if check in text:
                    text = text.replace(check, param)
            return text

        edited_text = text
        edited_text = edit(edited_text, "$radioname", str(song.description))
        edited_text = edit(edited_text, "$name", str(song.name))
        edited_text = edit(edited_text, "$authors", str(song.authors))
        edited_text = edit(edited_text, "$album", str(song.album))
        edited_text = edit(edited_text, "$album-count", str(song.album_count))
        edited_text = edit(edited_text, "$now-track", str(song.now_track_in_queue))
        edited_text = edit(edited_text, "$queue-count", str(song.count_tracks_in_queue))
        edited_text = edit(edited_text, "$minutes", str(song.minutes))
        edited_text = edit(edited_text, "$album-url", str(song.album_url))
        edited_text = edit(edited_text, "$track-url", str(song.link))
        edited_text = edit(edited_text, "$seconds", str(song.seconds).zfill(2))
        return edited_text
    
    def check_text_in_str(self, text: str) -> str | None:
        if text == '':
            return None
        return text

    def update(self, song: API):
        end = None
        t_time = settings.get('t_time', 2)
        if t_time:
            end = int(time() + song.seconds + song.minutes * 60)
        details = self.param_to_text(settings.get('tr_details'), song)
        state = self.param_to_text(settings.get('tr_state'), song)
        large_text = self.param_to_text(settings.get('tr_large_image'), song)
        small_text = self.param_to_text(settings.get('tr_small_image'), song)
        self.rpc.update(
            details=details,
            state=state, 
            large_text=large_text,
            small_text=small_text,
            large_image=song.icon,
            small_image=settings.get('icon'),
            buttons=self.__button(song, 'track'),
            end=end
        )
        debugger.addRequest(f'Установлен статус: {details=}, {state=}')

    def repeat(self, song: API, lastupdate):
        start = None
        end = None
        t_time = settings.get('t_time', 2)
        if t_time == 2:
            start = int(lastupdate)
        elif t_time == 1:
            end = int(time() + song.seconds + song.minutes * 60)
        details = self.param_to_text(settings.get('re_details'), song)
        state = self.param_to_text(settings.get('re_state'), song)
        large_text = self.param_to_text(settings.get('re_large_image'), song)
        small_text = self.param_to_text(settings.get('re_small_image'), song)
        self.rpc.update(
            details=details,
            state=state, 
            large_text=large_text,
            small_text=small_text,
            large_image=song.icon,
            small_image='https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Repeat.png',
            buttons=self.__button(song, 'repeat'),
            end=end,
            start=start
        )   
        debugger.addRequest(f'Статус переключен на повтор текущего трека.')

    def wave(self, song: API):
        w_time = settings.get('w_time', True)
        start = None
        if w_time:
            start = int(time())
        details = self.param_to_text(settings.get('ww_details'), song)
        state = self.param_to_text(settings.get('ww_state'), song)
        large_text = self.param_to_text(settings.get('ww_large_image'), song)
        small_text = self.param_to_text(settings.get('ww_small_image'), song)
        self.rpc.update(
            details=details,
            state=state, 
            large_text=large_text,
            small_text=small_text,
            large_image=settings.get('wave_icon'),
            small_image=settings.get('icon'),
            buttons=self.__button(song, 'wave'),
            start=start
        )
        debugger.addRequest(f'Установлен статус: {details=}, {state=}')

    def nodata(self, song: API):
        n_clear = settings.get('n_clear', False)
        timestamp = int(time())
        details = self.check_text_in_str(settings.get('no_details'))
        state = self.check_text_in_str(settings.get('no_state'))
        large_text = self.check_text_in_str(settings.get('no_large_image'))
        if not n_clear:
            self.rpc.update(
                details=details,
                state=state, 
                large_text=large_text,
                large_image=settings.get('icon'),
                buttons=self.__button(song, 'nodata'),
                start=timestamp
            )
        else:
            self.rpc.clear()
        debugger.addRequest(f'Установлен статус: {details=}, {state=}')
    def clear(self):
        self.rpc.clear()
        debugger.addRequest('Статус скрыт')

    def disconnect(self):
        self.rpc.close()