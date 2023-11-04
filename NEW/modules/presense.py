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
class Rpc():
    def clear():
        rpc.clear()
    def nodata(settings):
        n_clear = settings.get('n_clear', False)
        time = int(datetime.datetime.now().timestamp())
        if not n_clear:
            rpc.update(
                details="Нет данных о треке",
                state="Неизвестно",
                large_image='logo',
                large_text="RPC by Soto4ka37",
                start=time
            )
        else:
            rpc.clear()

    def radio(data, settings):
        w_time = settings.get('w_time', True)
        start = None
        if w_time:
            start = int((datetime.datetime.now()).timestamp())
        rpc.update(
            details="Слушает поток",
            state=f'"{data.name}"',
            large_image='mywave',
            small_image='logo',
            small_text='RPC by Soto4ka37',
            start=start,
        )
    def update(song, settings):
        end = None
        t_time = settings.get('t_time', 2)
        if t_time:
            end = int((datetime.datetime.now() + datetime.timedelta(minutes=song.minutes, seconds=song.seconds)).timestamp())
        rpc.update(
            details=f'{song.name}',
            state=f'{song.authors}', 
            large_image=song.icon,
            small_image='logo',
            large_text=f"{song.album} ({song.count} треков)",
            small_text=f'{song.minutes}:{song.seconds:0>2}',
            end=end,
            buttons=button(song, settings),
        )

    def repeat(song, settings, lastupdate):
        start = None
        end = None
        t_time = settings.get('t_time', 2)
        if t_time == 2:
            start = int(lastupdate.timestamp())
        elif t_time == 1:
            end = int((datetime.datetime.now() + datetime.timedelta(minutes=song.minutes, seconds=song.seconds)).timestamp())

        rpc.update(
            details=f'{song.name}',
            state=f'{song.authors}', 
            large_image=song.icon,
            small_image='repeat',
            large_text=f"{song.album} ({song.count} треков)",
            small_text=f'Трек повторяется',
            buttons=button(song, settings),
            end=end,
            start=start,
        )   