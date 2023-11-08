import datetime
from pypresence import Presence
rpc = Presence(client_id=1116090392123822080)
rpc.connect()

#        debug = settings.get('debug', False)
#        ping = settings.get('ping', 1)
#        t_time = settings.get('t_time', 2)
#        t_button = settings.get('t_button', True)
#        w_time = settings.get('w_time', True)
#        n_clear = settings.get('n_clear', False)
#        n_time = settings.get('n_time', True)

def button(song, settings):
    t_button = settings.get('t_button', True)
    button = None
    if t_button:
        button = [{"label": "Слушать", "url": f"{song.link}"}]
    return button

def strsong(text: str, song):
    if not text:
        return None
    def edit(text, string, param):
        if param:
            if string in text:
                text = text.replace(string, param)
        return text

    edited_text = text
    edited_text = edit(edited_text, "$name", str(song.name))
    edited_text = edit(edited_text, "$authors", str(song.authors))
    edited_text = edit(edited_text, "$album", str(song.album))
    edited_text = edit(edited_text, "$count", str(song.count))
    edited_text = edit(edited_text, "$minutes", str(song.minutes))
    edited_text = edit(edited_text, "$seconds", str(song.seconds).zfill(2))

    return edited_text


def strradio(text: str, radio):
    if not text:
        return None
    def edit(text, string, param):
        if param:
            if string in text:
                text = text.replace(string, param)
        return text

    edited_text = text
    edited_text = edit(edited_text, "$radioname", str(radio.name))

    return edited_text

class Rpc():
    def update(song, settings):
        end = None
        t_time = settings.get('t_time', 2)
        if t_time:
            end = int((datetime.datetime.now() + datetime.timedelta(minutes=song.minutes, seconds=song.seconds)).timestamp())
        details = strsong(settings.get('tr_details'), song)
        state = strsong(settings.get('tr_state'), song)
        large_text = strsong(settings.get('tr_large_image'), song)
        small_text = strsong(settings.get('tr_small_image'), song)
        rpc.update(
            details=details,
            state=state, 
            large_text=large_text,
            small_text=small_text,
            large_image=song.icon,
            small_image='logo',
            buttons=button(song, settings),
            end=end
        )

    def repeat(song, settings, lastupdate):
        start = None
        end = None
        t_time = settings.get('t_time', 2)
        if t_time == 2:
            start = int(lastupdate.timestamp())
        elif t_time == 1:
            end = int((datetime.datetime.now() + datetime.timedelta(minutes=song.minutes, seconds=song.seconds)).timestamp())
        details = strsong(settings.get('tr_details'), song)
        state = strsong(settings.get('tr_state'), song)
        large_text = strsong(settings.get('tr_large_image'), song)
        small_text = strsong(settings.get('tr_small_image'), song)
        rpc.update(
            details=details,
            state=state, 
            large_text=large_text,
            small_text=small_text,
            large_image=song.icon,
            small_image='repeat',
            buttons=button(song, settings),
            end=end,
            start=start
        )   

    def radio(radio, settings):
        w_time = settings.get('w_time', True)
        start = None
        if w_time:
            start = int((datetime.datetime.now()).timestamp())
        print(start)
        details = strradio(settings.get('ww_details'), radio)
        print(f'{details=}')
        state = strradio(settings.get('ww_state'), radio)
        print(f'{state=}')
        large_text = strradio(settings.get('ww_large_image'), radio)
        print(f'{large_text=}')
        small_text = strradio(settings.get('ww_small_image'), radio)
        print(f'{small_text=}')
        rpc.update(
            details=details,
            state=state, 
            large_text=large_text,
            small_text=small_text,
            large_image='mywave',
            small_image='logo',
            start=start
        )

    def nodata(settings):
        n_clear = settings.get('n_clear', False)
        time = int(datetime.datetime.now().timestamp())
        details = settings.get('no_details')
        state = settings.get('no_state')
        large_text = settings.get('no_large_image')
        if not n_clear:
            rpc.update(
                details=details,
                state=state, 
                large_text=large_text,
                large_image='logo',
                start=time
            )
        else:
            rpc.clear()

    def clear():
        rpc.clear()