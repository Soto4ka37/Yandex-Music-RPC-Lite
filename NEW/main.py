version = "v8.0"
import datetime
import time
from modules.presense import Rpc
from modules.data import save_settings, load_settings
from threading import Thread
import tkinter as tk
from tkinter import messagebox 
from PIL import Image, ImageTk
import requests
import sys
from io import BytesIO
import pystray
import webbrowser
from modules.api import Song, Radio
import os
def get_icon():
    response = requests.get("https://cdn.discordapp.com/attachments/1117022431748554782/1170439781730230292/RPC-Icon.ico")
    if response.status_code == 200:
        with open("icon.ico", "wb") as file:
            file.write(response.content)
    else:
        sys.exit()
if not os.path.exists('icon.ico'):
    get_icon()
settings = load_settings()
exit = True
settings_open = False
trayon = False
def check_updates(version):

    response = requests.get("https://api.github.com/repos/Soto4ka37/Yandex-Music-RPC-Lite/releases/latest")
    
    if response.status_code == 200:
        latest = response.json()
        latest_version = latest["tag_name"]
        if version != latest_version:
            answer = messagebox.askquestion("Версия устарела.", f"Версия программы устарела!\nИспользуется: {version} | Последняя: {latest_version}\n\nОткрыть GitHub?")
            if answer == "yes":
                webbrowser.open("https://github.com/Soto4ka37/Yandex-Music-RPC-Lite/releases/latest")
                sys.exit()
check_updates(version)

def gui():
    global name, author, change_image
    def open_settings_window():
        global settings_open, settings_window
        if settings_open:
            return
        def on_checkbox_button():
            settings['t_button'] = button_var.get()
            save_settings(settings)

        def on_timewave_button():
            settings['w_time'] = timewave_var.get()
            save_settings(settings)

        def on_clearnodata_button():
            settings['n_clear'] = clearnodata_var.get()
            save_settings(settings)

        def on_timenodata_button():
            settings['n_time'] = timenodata_var.get()
            save_settings(settings)

        def on_ping():
            settings['ping'] = pingvar.get()
            save_settings(settings)

        def on_option_selected(event):
            t_time = selected_option.get()
            if t_time == 'Выключить время': settings['t_time'] = 0
            if t_time == 'Автоповтор': settings['t_time'] = 1
            if t_time == 'Смена на "Прошло"': settings['t_time'] = 2
            save_settings(settings)

        def close_settings_window():
            global settings_open
            settings_open = False
            settings_window.destroy()

        settings_window = tk.Toplevel(root)
        settings_window.title("Настройки")
        settings_open = True
        settings_window.protocol("WM_DELETE_WINDOW", close_settings_window)
        lbl = tk.Label(settings_window, text="Производительность", font=("Arial Bold", 15))
        lbl.pack(anchor='w')

        lbl = tk.Label(settings_window, text="Задержка между запросами (Сек)")
        lbl.pack(anchor='w')
        pingvar = tk.IntVar()
        pingvar.set(settings.get('ping', 1))
        ping = tk.Spinbox(settings_window, textvariable=pingvar, from_=0, to=3, width=5, command=on_ping)  
        ping.pack(anchor='w')

        lbl = tk.Label(settings_window, text="Основные", font=("Arial Bold", 15))
        lbl.pack(anchor='w')

        lbl = tk.Label(settings_window, text="Время при окончании трека")
        lbl.pack(anchor='w')

        options = ['Выключить время', 'Автоповтор', 'Смена на "Прошло"']

        selected_option = tk.StringVar()
        selected_option.set(options[settings.get('t_time', 2)]) 

        option_menu = tk.OptionMenu(settings_window, selected_option, *options, command=on_option_selected)
        option_menu.pack(anchor="w")

        button_var = tk.BooleanVar(value=settings.get('t_button', True))
        button = tk.Checkbutton(settings_window, variable=button_var, text='Отображать кнопку "Слушать"', command=on_checkbox_button)
        button.pack(anchor="w")

        lbl = tk.Label(settings_window, text="Поток", font=("Arial Bold", 15))
        lbl.pack(anchor='w')

        timewave_var = tk.BooleanVar(value=settings.get('w_time', True))
        timewave = tk.Checkbutton(settings_window, variable=timewave_var, text="Подсчёт времени при прослушивании потока", command=on_timewave_button)
        timewave.pack(anchor="w")

        lbl = tk.Label(settings_window, text="Основные", font=("Arial Bold", 15))
        lbl.pack(anchor='w')
        
        clearnodata_var = tk.BooleanVar(value=settings.get('n_clear', False))
        clearnodata = tk.Checkbutton(settings_window, variable=clearnodata_var, text="Скрыть статус при неизвестном треке", command=on_clearnodata_button)
        clearnodata.pack(anchor="w")

        timenodata_var = tk.BooleanVar(value=settings.get('n_time', True))
        timenodata = tk.Checkbutton(settings_window, variable=timenodata_var, text="Подсчёт времени при неизвестном треке", command=on_timenodata_button)
        timenodata.pack(anchor="w")
        lbl = tk.Label(settings_window, text="*Настройки применяются при смене трека", font=("Arial Bold", 8))
        lbl.pack(anchor='w')

    def update_status():
        global lasttrack, lastradio, nowplaymode
        lasttrack = lastradio = nowplaymode = None
        if app_var.get() == 1:
            settings["on"] = True
            name.set("Загрузка...")
            change_image('https://music.yandex.ru/blocks/playlist-cover/playlist-cover_no_cover4.png')
            author.set("")
            save_settings(settings)
        else:
            settings["on"] = False
            name.set('СКРИПТ ВЫКЛЮЧЕН')
            change_image('https://media.discordapp.net/attachments/1117022431748554782/1117022461045772379/logo.png')
            author.set("")
            save_settings(settings)

    def change_image(url):
        response = requests.get(url)
        image_data = response.content

        image = Image.open(BytesIO(image_data))
        image = image.resize((75, 75))
        image = ImageTk.PhotoImage(image)

        image_label.config(image=image)
        image_label.photo = image

        del image


    def on_mouse_press(event):
        global x, y
        x, y = event.x_root - root.winfo_x(), event.y_root - root.winfo_y()

    def move_window(event):
        if x is not None and y is not None:
            x0, y0 = event.x_root, event.y_root
            root.geometry(f"+{x0 - x}+{y0 - y}")

    def quit_window(icon, item):
        global exit
        show_window(icon, item)
        settings['on'] = False
        root.destroy()
        exit = False
        sys.exit()

    def show_settings(icon, item):
        show_window(icon, item)
        open_settings_window()

    def show_window(icon, item):
        icon.stop()
        root.after(0,root.deiconify)
    def open_github(icon, item):
        webbrowser.open("https://github.com/Soto4ka37/Yandex-Music-RPC-Lite/")

    def withdraw_window():  
        global trayon, icon, settings_window, settings_open
        settings_open = False
        try:
            settings_window.destroy()
        except:
            pass
        if settings.get('on', False):
            root.withdraw()
            image = Image.open("icon.ico")
            menu = (pystray.MenuItem('Открыть', show_window, default=True), pystray.MenuItem('Настройки', show_settings), pystray.MenuItem('GitHub', open_github), pystray.MenuItem('Выход', quit_window))
            icon = pystray.Icon("name", image, f"RPC {version}", menu)
            trayon = True
            icon.run()
        else:
            trayon = False
            global exit
            settings['on'] = False
            root.destroy()
            exit = False
            sys.exit()

    root = tk.Tk()
    root.iconbitmap('icon.ico')
    menu = tk.Menu(root)
    menu.add_cascade(label='Открыть настройки', command=open_settings_window) 
    root.config(menu=menu)
    root.title(f"RPC")
    app_checkbox_state = settings.get('on', False)
    app_var = tk.BooleanVar(value=app_checkbox_state)
    app_checkbox = tk.Checkbutton(root, text="Connect", variable=app_var, command=update_status)

    name = tk.StringVar()
    author = tk.StringVar()
    
    name_label = tk.Label(root, textvariable=name)
    author_label = tk.Label(root, textvariable=author)
    image_label = tk.Label(root)

    update_status()

    image_label.grid(row=0, column=0, rowspan=3, sticky="w", padx=5, pady=5)
    app_checkbox.grid(row=0, column=1, sticky="w", padx=10)
    name_label.grid(row=1, column=1, sticky="w", padx=10)
    author_label.grid(row=2, column=1, sticky="w", padx=10)

    root.bind("<ButtonPress-1>", on_mouse_press)
    root.bind("<B1-Motion>", move_window)

    root.protocol("WM_DELETE_WINDOW", withdraw_window)

    root.mainloop()

def presense():
    global lasttrack, lastradio, nowplaymode, icon, trayon
    lasttrack = lastradio = nowplaymode = None
    while exit:
        if trayon:
            icon.notify(
            title='Скрыто в трей',
            message='Приложение работет в фоновом режиме',
        )
            trayon = False
        song = Song()
        radio = Radio()
        try:
            if settings.get("on"):
                song.update()
                radio.update()

                if song.done:
                    if song.link != lasttrack:
                        lasttrack = song.link
                        nowplaymode = None
                    if nowplaymode not in ["Track", "Repeat"]:
                        Rpc.update(song, settings)
                        if settings.get('on', False):
                            name.set(song.name)
                            author.set(song.authors)
                            change_image(song.icon)
                        lastupdate = datetime.datetime.now()
                        nowplaymode = "Track"
                    elif settings.get('t_time', 2) and nowplaymode == "Track":
                        r_time = (datetime.datetime.now() - lastupdate).total_seconds()
                        if r_time >= song.total:
                            Rpc.repeat(song, settings, lastupdate)
                            if settings.get('t_time', 2) == 1:
                                lastupdate = datetime.datetime.now()
                            elif settings.get('t_time', 2) == 2:
                                nowplaymode = "Repeat"

                elif radio.done and radio.type == "radio":
                    if radio.name != lastradio:
                        Rpc.radio(data=radio, settings=settings)
                        if settings.get('on', False):
                            name.set('Играет поток:')
                            author.set(radio.name)
                            change_image('https://cdn.discordapp.com/attachments/1117022431748554782/1170297064345829437/mywave.png')
                        lastradio = radio.name
                        nowplaymode = None

                else:
                    if nowplaymode != 'None':
                        Rpc.nodata(settings)
                        nowplaymode = 'None'
                        if settings.get('on', False):
                            name.set('Неизвестный трек')
                            author.set('')
                            change_image('https://music.yandex.ru/blocks/playlist-cover/playlist-cover_no_cover4.png')
                        #print(f'[Song] {song.error}')
                        #print(f'[Radio] {radio.error}')
            else:
                Rpc.clear()
                lasttrack = lastradio = nowplaymode = None
        except Exception as e:
            #print(f"[CRITICAL] {e}")
            pass
        time.sleep(settings.get('ping', 1))


if __name__ == "__main__":
    t1 = Thread(target=presense)
    t1.start()
    
    t2 = Thread(target=gui)
    t2.start()
    t1.join()
    t2.join()