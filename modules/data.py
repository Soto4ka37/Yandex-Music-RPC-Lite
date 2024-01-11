version = 'v9.1'
import json
import os
import requests
import sys
from tkinter import messagebox 

default = {
    "tr_details": "$name",
    "tr_state": "$authors",
    "tr_large_image": "$album ($album-count треков)",
    "tr_small_image": "$name ($minutes:$seconds)",
    "re_details": "$name",
    "re_state": "$authors",
    "re_large_image": "$album ($album-count треков)",
    "re_small_image": "Трек повторяется",
    "ww_details": "Играет поток",
    "ww_state": '"$radioname"',
    "ww_large_image": '',
    "ww_small_image": 'RPC by Soto4ka37',
    "no_details": "Нет данных",
    "no_state": "",
    "no_large_image": "RPC by Soto4ka37",

    "first_button_label": "Слушать",
    "first_button_url": "$track-url",
    "second_button_label": "",
    "second_button_url": "",
    "b1_track": True,
    "b1_repeat": True,
    "b1_wave": False,
    "b1_nodata": False,
    "b2_track": False,
    "b2_repeat": False,
    "b2_wave": False,
    "b2_nodata": False,

    "icon": 'https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-New.png',
    "wave_icon": 'https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Wave.gif',
    "wave_animated_icon": True,
    "ping": 5,
    "t_time": 2,
    "t_button": True,
    "w_time": True,
    "n_clear": False,
    "n_time": True,
    "on": False,
    "update": True,
    "image": True,
    "background": True,
    "token": "0"
}

appdata_path = os.getenv('APPDATA')
work_dir = os.path.join(appdata_path, 'YM-RPC')
if not os.path.exists(work_dir):
        os.makedirs(work_dir)

def get_file(path: str, url: str):
    if not os.path.exists(path):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(path, "wb") as file:
                    file.write(response.content)
            else:
                sys.exit()
        except:
            sys.exit()

icons_dir = os.path.join(work_dir, 'icons')
if not os.path.exists(icons_dir):
        os.makedirs(icons_dir)

new_image = os.path.join(icons_dir, 'new.png')
if not os.path.exists(new_image):
    get_file(new_image, "https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/IC-New.png")

old_image = os.path.join(icons_dir, 'old.png')
if not os.path.exists(old_image):
    get_file(old_image, "https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/IC-Old.png")

none_image = os.path.join(icons_dir, 'none.png')
if not os.path.exists(none_image):
    get_file(none_image, "https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/IC-None.png")

icon_path = os.path.join(icons_dir, 'icon.ico')
if not os.path.exists(icon_path):
    get_file(icon_path, "https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Icon.ico")

settings_path = os.path.join(work_dir, 'data.json')

def check_settings() -> bool:
    try:
        with open(settings_path, 'r') as file:
            settings = json.load(file)
        for key in default.keys():
            if key not in settings:
                messagebox.showerror("Ошибка чтения сохранений", "Данные используемые программой повреждены или устарели. Настройки утеряны.")
                return False
        return True
    except (FileNotFoundError, json.JSONDecodeError):
        return False

def load_settings() -> dict:
    if not check_settings():
        save_settings(default)
    with open(settings_path, 'r') as file:
        settings = json.load(file)
    return settings

def save_settings(settings: dict):
    with open(settings_path, 'w') as file:
        json.dump(settings, file, indent=4)


settings = load_settings()