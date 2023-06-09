from configparser import ConfigParser
from yandex_music import Client
from modules.getToken import token

config = ConfigParser()

config.read('info/config.ini')

if len(config.get("main","yandexmusictoken")) <= 2:
    print("[RPC] Получение токена.. Войдите в аккаунт в открывшимся окне")
    config.set("main", "yandexmusictoken", token.get_token())
    print("[RPC] Успешный запуск")
    with open("info/config.ini", "w") as config_file:
        config.write(config_file)
    
    client = Client(config.get("main", "yandexmusictoken")).init()
else:
    print("[RPC] Успешный запуск")
    client = Client(config.get("main", "yandexmusictoken")).init()

class MYAPI:
    def songTitle():
        lQ = client.queue(client.queues_list()[0].id)
        last_track_id = lQ.get_current_track()
        last_track = last_track_id.fetch_track()
        return last_track.title

    def songArtist():
        lQ = client.queue(client.queues_list()[0].id)
        lQid = lQ.get_current_track()
        last_track = lQid.fetch_track()
        return ', '.join(last_track.artists_name())
    
    def songLink():
        lQ = client.queue(client.queues_list()[0].id)
        lQid = lQ.get_current_track()
        lQlt = lQid.fetch_track()
        return f"https://music.yandex.ru/album/{lQlt['albums'][0]['id']}/track/{lQlt['id']}/"
        
    def songID():
        lQ = client.queue(client.queues_list()[0].id)
        return lQ.get_current_track()

    def songImage():
        queues = client.queues_list()
        lQ = client.queue(queues[0].id)
        lQid = lQ.get_current_track()
        lQlt = lQid.fetch_track()
        return "https://" + lQlt.cover_uri.replace("%%", "200x200")

    def songTime():
        track_id = client.queue(client.queues_list()[0].id)
        last_track_id = track_id.get_current_track()
        last_track = last_track_id.fetch_track()
        duration_min = str((last_track.duration_ms // (1000 * 60)) % 60)
        duration_sec = str((last_track.duration_ms // 1000) % 60)
        return f"{duration_min}:{duration_sec}"