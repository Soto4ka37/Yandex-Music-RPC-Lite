from configparser import ConfigParser

config = ConfigParser()
config.read('info/config.ini')
button = config.get("settings", "button")
if not (button == "0" or button == "1"):
    button = "1"

class BTNget:
    def btn(song):
        if button == "1":
            btn = [{"label": "Слушать", "url": f"{song[2]}"}]
        else:
            btn = None
        return btn