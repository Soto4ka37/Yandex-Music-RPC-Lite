version = "v8.2"

import os
from datetime import datetime
from time import sleep
from threading import Thread, Event

import pystray
import webbrowser
import requests
import tkinter as tk
from tkinter.ttk import Button, Spinbox, Radiobutton, Checkbutton, Label, Entry
from PIL import Image, ImageTk
from io import BytesIO

from modules.data import save_settings, load_settings, get_icon_path, get_icon
from modules.api import Song, Radio, run
run()
from modules.presense import Rpc
from modules.update import check_updates

updatepresense = True
settings_open = False
settings_text_open = False
need_notify = False

settings = load_settings()

icon_path = get_icon_path()
if not os.path.exists(icon_path):
    get_icon()

if settings.get('update'):
    check_updates(version)

def gui():
    global name, author, change_image
    def open_text_settings():
        def close_settings_window():
            global settings_text_open
            settings_text_open = False
            settings_text_window.destroy()
        def guide():
            webbrowser.open("https://github.com/Soto4ka37/Yandex-Music-RPC-Lite/tree/master/assets/guide.md")
        def save():
            global nowplaymode
            nowplaymode = None
            settings['tr_details'] = tr_details.get()
            settings['tr_state'] = tr_state.get()
            settings['tr_large_image'] = tr_large_image.get()
            settings['tr_small_image'] = tr_small_image.get()
            settings['re_details'] = re_details.get()
            settings['re_state'] = re_state.get()
            settings['re_large_image'] = re_large_image.get()
            settings['re_small_image'] = re_small_image.get()
            settings['ww_details'] = ww_details.get()
            settings['ww_state'] = ww_state.get()
            settings['ww_large_image'] = ww_large_image.get()
            settings['ww_small_image'] = ww_small_image.get()
            settings['no_details'] = no_details.get()
            settings['no_state'] = no_state.get()
            settings['no_large_image'] = no_large_image.get()
            close_settings_window()
        global settings_text_open, settings_text_window
        if settings_text_open:
            return
        settings_text_window = tk.Toplevel(window)
        settings_text_window.title("Редактор статуса")
        settings_text_open = True
        settings_text_window.protocol("WM_DELETE_WINDOW", close_settings_window)

        btn = Button(settings_text_window, text="Открыть гайд", command=guide, width=39)  
        btn.grid(row=0, column=0)  
        btn = Button(settings_text_window, text="Применить", command=save, width=17)  
        btn.grid(row=0, column=1, sticky="w")  

        lbl = Label(settings_text_window, text="При треке", font=("Arial Bold", 15))
        lbl.grid(row=1, column=0, sticky="w")

        lbl = Label(settings_text_window, text="Верхняя строчка")
        lbl.grid(row=2, column=1, sticky="w")
        tr_details = tk.StringVar()
        tr_details.set(settings.get('tr_details'))
        txt = Entry(settings_text_window, textvariable=tr_details, width=40) 
        txt.grid(row=2, column=0, sticky="w", padx=2, pady=1)

        lbl = Label(settings_text_window, text="Нижняя строчка")
        lbl.grid(row=3, column=1, sticky="w")
        tr_state = tk.StringVar()
        tr_state.set(settings.get('tr_state'))
        txt = Entry(settings_text_window, textvariable=tr_state, width=40) 
        txt.grid(row=3, column=0, sticky="w", padx=2, pady=1)

        lbl = Label(settings_text_window, text="Большая картинка")
        lbl.grid(row=4, column=1, sticky="w")
        tr_large_image = tk.StringVar()
        tr_large_image.set(settings.get('tr_large_image'))
        txt = Entry(settings_text_window, textvariable=tr_large_image, width=40) 
        txt.grid(row=4, column=0, sticky="w", padx=2, pady=1)

        lbl = Label(settings_text_window, text="Маленькая картинка")
        lbl.grid(row=5, column=1, sticky="w")
        tr_small_image = tk.StringVar()
        tr_small_image.set(settings.get('tr_small_image'))
        txt = Entry(settings_text_window, textvariable=tr_small_image, width=40) 
        txt.grid(row=5, column=0, sticky="w", padx=2, pady=1)

        lbl = Label(settings_text_window, text="При повторе трека", font=("Arial Bold", 15))
        lbl.grid(row=6, column=0, sticky="w")

        lbl = Label(settings_text_window, text="Верхняя строчка")
        lbl.grid(row=7, column=1, sticky="w")
        re_details = tk.StringVar()
        re_details.set(settings.get('re_details'))
        txt = Entry(settings_text_window, textvariable=re_details, width=40) 
        txt.grid(row=7, column=0, sticky="w", padx=2, pady=1)

        lbl = Label(settings_text_window, text="Нижняя строчка")
        lbl.grid(row=8, column=1, sticky="w")
        re_state = tk.StringVar()
        re_state.set(settings.get('re_state'))
        txt = Entry(settings_text_window, textvariable=re_state, width=40) 
        txt.grid(row=8, column=0, sticky="w", padx=2, pady=1)

        lbl = Label(settings_text_window, text="Большая картинка")
        lbl.grid(row=9, column=1, sticky="w")
        re_large_image = tk.StringVar()
        re_large_image.set(settings.get('re_large_image'))
        txt = Entry(settings_text_window, textvariable=re_large_image, width=40) 
        txt.grid(row=9, column=0, sticky="w", padx=2, pady=1)

        lbl = Label(settings_text_window, text="Маленькая картинка")
        lbl.grid(row=10, column=1, sticky="w")
        re_small_image = tk.StringVar()
        re_small_image.set(settings.get('re_small_image'))
        txt = Entry(settings_text_window, textvariable=re_small_image, width=40) 
        txt.grid(row=10, column=0, sticky="w", padx=2, pady=1)

        lbl = Label(settings_text_window, text="При потоке", font=("Arial Bold", 15))
        lbl.grid(row=11, column=0, sticky="w")

        lbl = Label(settings_text_window, text="Верхняя строчка")
        lbl.grid(row=12, column=1, sticky="w")
        ww_details = tk.StringVar()
        ww_details.set(settings.get('ww_details'))
        txt = Entry(settings_text_window, textvariable=ww_details, width=40) 
        txt.grid(row=12, column=0, sticky="w", padx=2, pady=1)

        lbl = Label(settings_text_window, text="Нижняя строчка")
        lbl.grid(row=13, column=1, sticky="w")
        ww_state = tk.StringVar()
        ww_state.set(settings.get('ww_state'))
        txt = Entry(settings_text_window, textvariable=ww_state, width=40) 
        txt.grid(row=13, column=0, sticky="w", padx=2, pady=1)

        lbl = Label(settings_text_window, text="Большая картинка")
        lbl.grid(row=14, column=1, sticky="w")
        ww_large_image = tk.StringVar()
        ww_large_image.set(settings.get('ww_large_image'))
        txt = Entry(settings_text_window, textvariable=ww_large_image, width=40) 
        txt.grid(row=14, column=0, sticky="w", padx=2, pady=1)

        lbl = Label(settings_text_window, text="Маленькая картинка")
        lbl.grid(row=15, column=1, sticky="w")
        ww_small_image = tk.StringVar()
        ww_small_image.set(settings.get('ww_small_image'))
        txt = Entry(settings_text_window, textvariable=ww_small_image, width=40) 
        txt.grid(row=15, column=0, sticky="w", padx=2, pady=1)

        lbl = Label(settings_text_window, text="При неизвестном треке", font=("Arial Bold", 15))
        lbl.grid(row=16, column=0, sticky="w")

        lbl = Label(settings_text_window, text="Верхняя строчка")
        lbl.grid(row=17, column=1, sticky="w")
        no_details = tk.StringVar()
        no_details.set(settings.get('no_details'))
        txt = Entry(settings_text_window, textvariable=no_details, width=40) 
        txt.grid(row=17, column=0, sticky="w", padx=2, pady=1)

        lbl = Label(settings_text_window, text="Нижняя строчка")
        lbl.grid(row=18, column=1, sticky="w")
        no_state = tk.StringVar()
        no_state.set(settings.get('no_state'))
        txt = Entry(settings_text_window, textvariable=no_state, width=40) 
        txt.grid(row=18, column=0, sticky="w", padx=2, pady=1)

        lbl = Label(settings_text_window, text="Большая картинка")
        lbl.grid(row=19, column=1, sticky="w")
        no_large_image = tk.StringVar()
        no_large_image.set(settings.get('no_large_image'))
        txt = Entry(settings_text_window, textvariable=no_large_image, width=40) 
        txt.grid(row=19, column=0, sticky="w", padx=2, pady=1)

    def open_settings():
        global settings_open, settings_text_window, nowplaymode
        if settings_open:
            return
        def on_button():
            global nowplaymode
            nowplaymode = None
            settings['t_button'] = button_var.get()
            save_settings(settings)

        def on_timewave():
            global nowplaymode
            nowplaymode = None
            settings['w_time'] = timewave_var.get()
            save_settings(settings)

        def on_clearnodata():
            global nowplaymode
            nowplaymode = None
            settings['n_clear'] = clearnodata_var.get()
            save_settings(settings)

        def on_timenodata():
            global nowplaymode
            nowplaymode = None
            settings['n_time'] = timenodata_var.get()
            save_settings(settings)

        def on_ping():
            settings['ping'] = pingvar.get()
            save_settings(settings)

        def on_updatecheck():
            settings['update'] = updatecheck_var.get()
            save_settings(settings)

        def on_updateimage():
            settings['image'] = updateimage_var.get()
            save_settings(settings)

        def on_background():
            settings['background'] = background_var.get()
            save_settings(settings)

        def on_timerb():
            global nowplaymode
            nowplaymode = None
            t_time = time_rbvar.get()
            settings['t_time'] = t_time
            save_settings(settings)

        def close_settings_window():
            global settings_open
            settings_open = False
            settings_window.destroy()

        settings_window = tk.Toplevel(window)
        settings_window.title("Настройки")
        settings_open = True
        settings_window.protocol("WM_DELETE_WINDOW", close_settings_window)
        lbl = Label(settings_window, text="Производительность", font=("Arial Bold", 15))
        lbl.grid(row=0, column=0, sticky="w")
        updatecheck_var = tk.BooleanVar(value=settings.get('update', True))
        updatecheck = Checkbutton(settings_window, variable=updatecheck_var, text="Проверять обновления при запуске", command=on_updatecheck)
        updatecheck.grid(row=1, column=0, sticky="w")

        updateimage_var = tk.BooleanVar(value=settings.get('image', True))
        updateimage = Checkbutton(settings_window, variable=updateimage_var, text="Обновлять картинку в приложении (Не влияет на статус)", command=on_updateimage)
        updateimage.grid(row=2, column=0, sticky="w")
        
        background_var = tk.BooleanVar(value=settings.get('background', False))
        background = Checkbutton(settings_window, variable=background_var, text="Разрешить работу в фоновом режиме", command=on_background)
        background.grid(row=3, column=0, sticky="w")

        lbl = Label(settings_window, text="Задержка между запросами (секунды)")
        lbl.grid(row=4, column=0, sticky="w")

        pingvar = tk.IntVar()
        pingvar.set(settings.get('ping', 1))
        ping = Spinbox(settings_window, textvariable=pingvar, from_=0, to=3, width=8, command=on_ping)
        ping.grid(row=5, column=0, sticky="w", padx=2)

        lbl = Label(settings_window, text="Основные", font=("Arial Bold", 15))
        lbl.grid(row=6, column=0, sticky="w")

        lbl = Label(settings_window, text="При окончании длинны трека: ")
        lbl.grid(row=7, column=0, sticky="w")

        time_rbvar = tk.IntVar()
        time_rbvar.set(settings.get('t_time'))

        time_rb = Radiobutton(settings_window, variable=time_rbvar, text='Выключить время', value=0, command=on_timerb)  
        time_rb.grid(row=8, column=0, sticky="w")

        time_rb1 = Radiobutton(settings_window, variable=time_rbvar, text='Автоповтор', value=1, command=on_timerb)  
        time_rb1.grid(row=9, column=0, sticky="w")

        time_rb2 = Radiobutton(settings_window, variable=time_rbvar, text='Смена на "Прошло"', value=2, command=on_timerb)  
        time_rb2.grid(row=10, column=0, sticky="w")

        button_var = tk.BooleanVar(value=settings.get('t_button', True))
        button = Checkbutton(settings_window, variable=button_var, text='Отображать кнопку "Слушать"', command=on_button)
        button.grid(row=11, column=0, sticky="w")

        lbl = Label(settings_window, text="Поток", font=("Arial Bold", 15))
        lbl.grid(row=12, column=0, sticky="w")

        timewave_var = tk.BooleanVar(value=settings.get('w_time', True))
        timewave = Checkbutton(settings_window, variable=timewave_var, text="Считать время при прослушивании потока", command=on_timewave)
        timewave.grid(row=13, column=0, sticky="w")

        lbl = Label(settings_window, text="Основные", font=("Arial Bold", 15))
        lbl.grid(row=14, column=0, sticky="w")
        
        clearnodata_var = tk.BooleanVar(value=settings.get('n_clear', False))
        clearnodata = Checkbutton(settings_window, variable=clearnodata_var, text="Скрыть статус при неизвестном треке", command=on_clearnodata)
        clearnodata.grid(row=15, column=0, sticky="w")

        timenodata_var = tk.BooleanVar(value=settings.get('n_time', True))
        timenodata = Checkbutton(settings_window, variable=timenodata_var, text="Считать время при неизвестном треке", command=on_timenodata)
        timenodata.grid(row=16, column=0, sticky="w")

    def update_status():
        global lasttrack, lastradio, nowplaymode
        lasttrack = lastradio = nowplaymode = None
        if app_var.get() == 1:
            settings["on"] = True
            name.set("Загрузка...")
            if settings.get("image"):
                change_image('https://music.yandex.ru/blocks/playlist-cover/playlist-cover_no_cover4.png')
            author.set("")
            save_settings(settings)
        else:
            settings["on"] = False
            name.set('Отключено')
            if settings.get("image"):
                change_image('https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Icon.png')
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

    def quit_window(icon, item):
        global updatepresense
        show_window(icon, item)
        window.destroy()
        settings['on'] = False
        updatepresense = False

    def show_settings(icon, item):
        show_window(icon, item)
        open_settings()

    def show_window(icon, item):
        icon.stop()
        window.after(0,window.deiconify)

    def open_github(icon, item):
        webbrowser.open("https://github.com/Soto4ka37/Yandex-Music-RPC-Lite/")

    def withdraw_window():  
        global need_notify, icon, settings_window, settings_open
        settings_open = False
        try:
            settings_window.destroy()
        except:
            pass
        if settings.get('on', False) and settings.get('background'):
            window.withdraw()
            image = Image.open(icon_path)
            menu = (pystray.MenuItem('Открыть', show_window, default=True), pystray.MenuItem('Настройки', show_settings), pystray.MenuItem('GitHub', open_github), pystray.MenuItem('Выход', quit_window))
            icon = pystray.Icon("name", image, f"RPC {version}", menu)
            need_notify = True
            icon.run()
        else:
            global updatepresense
            window.destroy()
            settings['on'] = False
            updatepresense = False
    window = tk.Tk()
    window.iconbitmap(icon_path)
    menu = tk.Menu(window)
    window.config(menu=menu)
    window.title(f"RPC")
    app_checkbox_state = settings.get('on', False)
    app_var = tk.BooleanVar(value=app_checkbox_state)
    app_checkbox = Checkbutton(window, text="Connect", variable=app_var, command=update_status)

    name = tk.StringVar()
    author = tk.StringVar()
    
    name_label = Label(window, textvariable=name)
    author_label = Label(window, textvariable=author)
    image_label = Label(window)

    if not settings.get("image"):
        change_image('https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Icon.png')
    update_status()

    btn = Button(window, text="Настройки", command=open_settings)  
    btn.grid(row=0, column=0)  
    btn = Button(window, text="Редактор текста", command=open_text_settings)  
    btn.grid(row=0, column=1, sticky="w", padx=5)  

    image_label.grid(row=1, column=0, rowspan=3, sticky="w", padx=5, pady=5)
    app_checkbox.grid(row=1, column=1, sticky="w", padx=5)
    name_label.grid(row=2, column=1, sticky="w", padx=5)
    author_label.grid(row=3, column=1, sticky="w", padx=5)
    def on_drag_start(event):
        global drag_data
        drag_data = {'x': event.x_root - window.winfo_x(), 'y': event.y_root - window.winfo_y()}

    def on_drag_motion(event):
        def move_window(event):
            window.geometry(f"+{event.x_root - drag_data['x']}+{event.y_root - drag_data['y']}")
        window.after(10, move_window, event)


    window.protocol("WM_DELETE_WINDOW", withdraw_window)
    window.bind("<Button-1>", on_drag_start)
    window.bind("<B1-Motion>", on_drag_motion)
    window.mainloop()

def presense():
    global lasttrack, lastradio, nowplaymode, icon, need_notify
    lasttrack = lastradio = nowplaymode = None
    while updatepresense:
        if need_notify:
            icon.notify(
            title='Скрыто в трей',
            message='Приложение работет в фоновом режиме',
        )
            need_notify = False
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
                            if settings.get('image'):
                                change_image(song.icon)
                        lastupdate = datetime.now()
                        nowplaymode = "Track"
                    elif settings.get('t_time', 2) and nowplaymode == "Track":
                        r_time = (datetime.now() - lastupdate).total_seconds()
                        if r_time >= song.total:
                            Rpc.repeat(song, settings, lastupdate)
                            if settings.get('t_time', 2) == 1:
                                lastupdate = datetime.now()
                            elif settings.get('t_time', 2) == 2:
                                nowplaymode = "Repeat"

                elif radio.done and radio.type == "radio":
                    if radio.name != lastradio:
                        Rpc.radio(radio=radio, settings=settings)
                        if settings.get('on', False):
                            name.set('Играет поток:')
                            author.set(radio.name)
                            if settings.get('image'):
                                change_image('https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Wave.png')
                        lastradio = radio.name
                        nowplaymode = None

                else:
                    if nowplaymode != 'None':
                        Rpc.nodata(settings)
                        nowplaymode = 'None'
                        if settings.get('on', False):
                            name.set('Неизвестный трек')
                            author.set('')
                            if settings.get('image'):
                                change_image('https://music.yandex.ru/blocks/playlist-cover/playlist-cover_no_cover4.png')
                        #print(f'[Song] {song.error}')
                        #print(f'[Radio] {radio.error}')
            else:
                Rpc.clear()
                lasttrack = lastradio = nowplaymode = None
        except Exception as e:
            #print(f"[CRITICAL] {e}")
            pass
        sleep(settings.get('ping', 1))

class StoppableThread(Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
    
if __name__ == "__main__":
    t1 = Thread(target=presense)
    t1.start()
    
    t2 = Thread(target=gui)
    t2.start()
    
    t1.join()