from configparser import ConfigParser
from yandex_music import Client
config = ConfigParser()
config.read('settings.ini')

client = Client(config.get("sys", "yandexmusictoken")).init()
while True:
    try:
        try:
            test = client.queue(client.queues_list()[0].id)
        except Exception as e:
            print(e)
            test = client.queues_list()[0]
            wave = test['context']['description']
            print(wave)
        print(test)
        input("Всё")
    except:
        input("Пусто")