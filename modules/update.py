import requests
import sys
import webbrowser
from tkinter import messagebox

def check_updates(version):
    response = requests.get("https://api.github.com/repos/Soto4ka37/Yandex-Music-RPC-Lite/releases/latest", timeout=5)
    if response.status_code == 200:
        latest = response.json()
        latest_version = latest["tag_name"]
        if version != latest_version:
            answer = messagebox.askquestion("Версия устарела.", f"Версия программы устарела!\nТекущая: {version} | Последняя: {latest_version}\n\nОткрыть GitHub?")
            if answer == "yes":
                webbrowser.open("https://github.com/Soto4ka37/Yandex-Music-RPC-Lite/releases/latest")
                sys.exit()