from configparser import ConfigParser
from yandex_music import Client
from modules.getToken import token

config = ConfigParser()

config.read('info/config.ini')

if len(config.get("main","yandexmusictoken")) <= 2:
    print("[RPC] Получение токена.. Войдите в аккаунт в открывшимся окне")
    config.set("main", "yandexmusictoken", token.get_token())
    print("[RPC] Токен получен и сохранён в config.ini.")
    with open("info/config.ini", "w") as config_file:
        config.write(config_file)
    
    client = Client(config.get("main", "yandexmusictoken")).init()
else:
    print("[RPC] Успешный запуск")
    client = Client(config.get("main", "yandexmusictoken")).init()

class MYAPI:
    def song():
        lQ = client.queue(client.queues_list()[0].id)
        last_track_id = lQ.get_current_track()
        last_track = last_track_id.fetch_track()
        lQlt = last_track_id.fetch_track()
        duration_min = str((last_track.duration_ms // (1000 * 60)) % 60)
        duration_sec = str((last_track.duration_ms // 1000) % 60)
        return last_track.title, ', '.join(last_track.artists_name()), f"https://music.yandex.ru/album/{lQlt['albums'][0]['id']}/track/{lQlt['id']}/", lQ.get_current_track(), "https://" + lQlt.cover_uri.replace("%%", "200x200"), f"{duration_min}:{duration_sec:0>2}"

    # song[0] - Название трека
    # song[1] - Автор трека
    # song[2] - Ссылка на трек
    # song[3] - ID трека
    # song[4] - Картинка трека
    # song[5] - Длинна трека (Минуты:Секунды)
