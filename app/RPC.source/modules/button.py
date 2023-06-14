from configparser import ConfigParser

config = ConfigParser()
config.read('info/config.ini')
button = config.get("settings", "button")
if not (button == "0" or button == "1"):
    print('[ОШИБКА] button НЕ УСТАНОВЛЕН ИЛИ УСТАНОВЛЕН НЕ ПРАВИЛЬНО!')
    button = "1"
    print('[Решение ошибки] Установлен режим по умолчанию (button = 1) для этой сессии, укажите правильный режим в info/conifg.ini')

class BTNget:
    def btn(song):
        if button == "1":
            btn = [{"label": "Слушать", "url": f"{song[2]}"}]
        else:
            btn = None
        return btn