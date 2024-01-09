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
    "re_large_image": "",
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

    "icon": 'https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Default.png',
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


def get_icon_path() -> str:
    appdata_path = os.getenv('APPDATA')
    ym_rpc_dir = os.path.join(appdata_path, 'YM-RPC')
    return os.path.join(ym_rpc_dir, 'icon.ico')

def get_settings_path() -> str:
    appdata_path = os.getenv('APPDATA')
    ym_rpc_dir = os.path.join(appdata_path, 'YM-RPC')
    if not os.path.exists(ym_rpc_dir):
        os.makedirs(ym_rpc_dir)
    return os.path.join(ym_rpc_dir, 'data.json')

icon_path = get_icon_path()
settings_path = get_settings_path()

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

def get_icon():
    if not os.path.exists(icon_path):
        response = requests.get("https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Icon.ico")
        if response.status_code == 200:
            with open(icon_path, "wb") as file:
                file.write(response.content)
        else:
            sys.exit()

settings = load_settings()