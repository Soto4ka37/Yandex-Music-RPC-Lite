from time import time
from pypresence import Presence
from modules.api import API
from modules.debug import Debug

class RPC:
    def __init__(self):
            debug = '[ПОДКЛЮЧЕНИЕ К ДИСКОРДУ]\n'
            try:
                self.rpc = Presence(client_id=1116090392123822080)
                self.rpc.connect()
                debug = debug + 'Удачно'
            except Exception as e:
                self.rpc = None
                debug = debug + f'Ошибка: {e}'
            Debug.add(debug)

    def __button(self, song: API, settings: dict):
        t_button = settings.get('t_button', True)
        button = None
        if t_button:
            button = [{"label": "Слушать", "url": f"{song.link}"}]
        return button

    def param_to_text(self, text: str, song: API) -> str:
        if not text:
            return None
        def edit(text, string, param):
            if param:
                if string in text:
                    text = text.replace(string, param)
            return text

        edited_text = text
        edited_text = edit(edited_text, "$radioname", str(song.description))
        edited_text = edit(edited_text, "$name", str(song.name))
        edited_text = edit(edited_text, "$authors", str(song.authors))
        edited_text = edit(edited_text, "$album", str(song.album))
        edited_text = edit(edited_text, "$count", str(song.count))
        edited_text = edit(edited_text, "$minutes", str(song.minutes))
        edited_text = edit(edited_text, "$seconds", str(song.seconds).zfill(2))

        return edited_text

    def update(self, song: API, settings: dict):
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
            small_image='logo',
            buttons=self.__button(song, settings),
            end=end
        )
        Debug.add(f'[DISCORD] [Обновлён статус]\n{song.name=}\n{song.authors=}\n{song.description=}')

    def repeat(self, song: API, settings: dict, lastupdate):
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
            small_image='repeat',
            buttons=self.__button(song, settings),
            end=end,
            start=start
        )   
        Debug.add(f'[DISCORD] [Обновлён статус]\nРежим повтора активирован')

    def song(self, song: API, settings: dict):
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
            large_image='mywave',
            small_image='logo',
            start=start
        )
        Debug.add(f'[DISCORD] [Обновлён статус]\n{song.name=}\n{song.authors=}\n{song.description=}')

    def nodata(self, settings: dict):
        n_clear = settings.get('n_clear', False)
        timestamp = int(time())
        details = settings.get('no_details')
        state = settings.get('no_state')
        large_text = settings.get('no_large_image')
        if not n_clear:
            self.rpc.update(
                details=details,
                state=state, 
                large_text=large_text,
                large_image='logo',
                start=timestamp
            )
        else:
            self.rpc.clear()
        Debug.add(f'[DISCORD] [Обновлён статус]\nНеизвестный трек')
    def clear(self):
        self.rpc.clear()
        Debug.add(f'[DISCORD] [Статус очищен]')

    def disconnect(self):
        self.rpc.close()
        Debug.add(f'[DISCORD] Соединение разоравно пользователем')