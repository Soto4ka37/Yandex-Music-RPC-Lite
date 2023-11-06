import json
import os
import requests
import sys

default = {
  "ping": 1,
  "t_time": 2,
  "t_button": True,
  "w_time": True,
  "n_clear": False,
  "n_time": True,
  "on": False,
  "update": True,
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
        response = requests.get("https://cdn.discordapp.com/attachments/1117022431748554782/1170439781730230292/RPC-Icon.ico")
        if response.status_code == 200:
            with open(icon_path, "wb") as file:
                file.write(response.content)
        else:
            sys.exit()

