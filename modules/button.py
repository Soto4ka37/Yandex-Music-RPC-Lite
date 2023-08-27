from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
button = config.get("settings", "button", raw=True)
if button not in ["True", "False"]:
    import colorama
    colorama.init()
    print(colorama.Fore.RED + '[Предупреждение] "button" не правильно установлен! Использую "True" как режим по умолчанию!' + colorama.Style.RESET_ALL)
    colorama.deinit()
    button = True
else:
    if button == "False":
        button = False
    else:
        button = True

class Button:
    def button(song):
        if button:
            btn = [{"label": "Слушать", "url": f"{song[2]}"}]
        else:
            btn = None
        return btn