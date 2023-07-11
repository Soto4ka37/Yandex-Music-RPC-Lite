from configparser import ConfigParser
from yandex_music import Client
from modules.getToken import UpdateToken

config = ConfigParser()

config.read('info/config.ini')

if len(config.get("main", "yandexmusictoken")) <= 2:
    token = UpdateToken()
    if token != "0":
        config.set("main", "yandexmusictoken", token)
    else:
        config.set("main", "yandexmusictoken", "0")
    with open("info/config.ini", "w") as config_file:
        config.write(config_file)

    client = Client(config.get("main", "yandexmusictoken")).init()
else:
    client = Client(config.get("main", "yandexmusictoken")).init()

class MYAPI:
    def song():
        lQ = client.queue(client.queues_list()[0].id)
        last_track_id = lQ.get_current_track()
        last_track = last_track_id.fetch_track()
        lQlt = last_track_id.fetch_track()
        duration_min = ((last_track.duration_ms // (1000 * 60)) % 60)
        duration_sec = ((last_track.duration_ms // 1000) % 60)
        duration_raw = ((last_track.duration_ms // 1000))
        return last_track.title, ', '.join(last_track.artists_name()), f"https://music.yandex.ru/album/{lQlt['albums'][0]['id']}/track/{lQlt['id']}/", lQ.get_current_track(), "https://" + lQlt.cover_uri.replace("%%", "200x200"), duration_min, duration_sec, duration_raw

    # song[0] - Название трека
    # song[1] - Автор трека
    # song[2] - Ссылка на трек
    # song[3] - ID трека
    # song[4] - Картинка трека
    # song[5] - Длинна трека (Минуты)
    # song[6] - Длинна трека (Секунды)
    # song[7] - Длинна трека (Только секунды)
