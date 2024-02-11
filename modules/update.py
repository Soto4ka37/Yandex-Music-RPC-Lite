import requests
import sys
import webbrowser
from tkinter import messagebox
from modules.debugger import addError, addInfo

def check_versions(old: str, new: str) -> bool:
    def normalize(v):
        return [int(x) for x in v.split(".")]

    v1 = normalize(old[1:])
    v2 = normalize(new[1:])

    while len(v1) < len(v2):
        v1.append(0)
    while len(v2) < len(v1):
        v2.append(0)

    if v1 < v2:
        return True
    elif v1 > v2:
        return False
    else:
        return False


def check_updates(version: str):
    try:
        response = requests.get("https://api.github.com/repos/Soto4ka37/Yandex-Music-RPC-Lite/releases/latest", timeout=5)
        if response.status_code == 200:
            latest = response.json()
            latest_version = latest["tag_name"]
            addInfo(f'Последняя версия программы: {latest_version}')
            if check_versions(version, latest_version):
                answer = messagebox.askquestion("Версия устарела.", f"Версия программы устарела!\nТекущая: {version} | Последняя: {latest_version}\n\nОткрыть GitHub?")
                if answer == "yes":
                    webbrowser.open("https://github.com/Soto4ka37/Yandex-Music-RPC-Lite/releases/latest")
                    sys.exit()
    except:
        addError('Не удалось проверить обновления!')