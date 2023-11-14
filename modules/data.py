import json
import os
import requests
import sys
from tkinter import messagebox 

default = {
    "tr_details": "$name",
    "tr_state": "$authors",
    "tr_large_image": "$album ($count треков)",
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

    "ping": 1,
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

def get_settings_path():
    appdata_path = os.getenv('APPDATA')
    ym_rpc_dir = os.path.join(appdata_path, 'YM-RPC')
    if not os.path.exists(ym_rpc_dir):
        os.makedirs(ym_rpc_dir)
    return os.path.join(ym_rpc_dir, 'data.json')

def check_settings():
    settings_path = get_settings_path()
    try:
        with open(settings_path, 'r') as file:
            settings = json.load(file)
        for key in default.keys():
            if key not in settings:
                messagebox.showerror("Данные утеряны", "Файл хранящий данные был повреждён. Насройки утеряны. Требуется повторная авторизация.")
                return False
        return True
    except (FileNotFoundError, json.JSONDecodeError):
        return False

def load_settings():
    if not check_settings():
        save_settings(default)
    settings_path = get_settings_path()
    with open(settings_path, 'r') as file:
        settings = json.load(file)
    return settings

def save_settings(settings):
    settings_path = get_settings_path()
    with open(settings_path, 'w') as file:
        json.dump(settings, file, indent=4)

def get_icon_path():
    appdata_path = os.getenv('APPDATA')
    ym_rpc_dir = os.path.join(appdata_path, 'YM-RPC')
    return os.path.join(ym_rpc_dir, 'icon.ico')

def get_icon():
    icon_path = get_icon_path()
    if not os.path.exists(icon_path):
        response = requests.get("https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Icon.ico")
        if response.status_code == 200:
            with open(icon_path, "wb") as file:
                file.write(response.content)
        else:
            sys.exit()

