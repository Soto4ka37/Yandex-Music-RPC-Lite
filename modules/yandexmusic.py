from configparser import ConfigParser
from yandex_music import Client
from modules.getToken import UpdateToken

config = ConfigParser()

config.read('settings.ini')

if len(config.get("sys", "yandexmusictoken")) <= 2:
    token = UpdateToken()
    if token != "0":
        config.set("sys", "yandexmusictoken", token)
    else:
        config.set("sys", "yandexmusictoken", "0")
    with open("settings.ini", "w") as config_file:
        config.write(config_file)

    client = Client(token).init()
else:
    client = Client(config.get("sys", "yandexmusictoken")).init()

class MYAPI:
    def radio():
        list = client.queues_list()[0]
        description = list['context']['description']
        return description
    
    def song():
        queue = client.queue(client.queues_list()[0].id)
        last_track_id = queue.get_current_track()
        last_track = last_track_id.fetch_track()
        duration = last_track.duration_ms
        duration_min = ((duration // (1000 * 60)) % 60)
        duration_sec = ((duration // 1000) % 60)
        duration_raw = ((duration // 1000))

        album = last_track.albums
        album_name = album[0]['title']
        track_count = album[0]['track_count']
        name = last_track.title
        artists = ', '.join(last_track.artists_name())
        link = f"https://music.yandex.ru/album/{last_track['albums'][0]['id']}/track/{last_track['id']}/"
        id = last_track['id']
        icon = "https://" + last_track.cover_uri.replace("%%", "200x200")
            
        # song[0] - Название трека
        # song[1] - Автор трека
        # song[2] - Ссылка на трек
        # song[3] - ID трека
        # song[4] - Картинка трека
        # song[5] - Длинна трека (Минуты)
        # song[6] - Длинна трека (Секунды)
        # song[7] - Длинна трека (Только секунды)
        # song[8] - Название альбома
        # song[9] - Количество треков в альбоме

        return name, artists, link, id, icon, duration_min, duration_sec, duration_raw, album_name, track_count