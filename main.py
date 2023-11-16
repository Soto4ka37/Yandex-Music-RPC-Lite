version = "v8.2.3"
from time import sleep, time

import traceback
import os
from threading import Thread
import pystray
import webbrowser
import requests
import tkinter as tk
from tkinter.ttk import Button, Spinbox, Radiobutton, Checkbutton, Label, Entry, Scrollbar
from PIL import Image, ImageTk
from io import BytesIO
from platform import system, version as v


from modules.debug import Debug
Debug.add('[ОТКЛАДКА ЗАПУЩЕНА]')
from modules.data import save_settings, load_settings, get_icon_path, get_icon
from modules.api import getclient, API
from modules.presense import RPC
from modules.update import check_updates
lastclick = 0
mainloop = True
settings_open = settings_text_open = need_notify = debug_opened = nowindow = rpc = None # Ебучие глобальные переменные

settings = load_settings()
icon_path = get_icon_path()

Debug.add(f"Операционная система: {system()} {v()}")
if not os.path.exists(icon_path):
    get_icon()

if settings.get('update'):
    check_updates(version)


def gui():
    '''
    Интерфейс
    '''
    global name, author, change_image, show_window, app_var
    def open_debug():
        class DebugWindow:
            def __init__(self, root: tk.Tk):
                global debug_opened
                debug_opened = True
                self.root = root
                self.root.title("Меню откладки")

                self.text_area = tk.Text(root, wrap="word", state="normal", height=25, width=40)
                initial_text = Debug.get_str()
                self.text_area.insert("1.0", initial_text)
                self.text_area.config(state="disabled")
                
                scroll_y = Scrollbar(root, orient="vertical", command=self.text_area.yview)
                scroll_y.grid(row=0, column=1, sticky="nsew")
                self.text_area.config(yscrollcommand=scroll_y.set)
                
                copy_button = Button(root, text="Копировать", command=self.copy_text)
                copy_button.grid(row=1, column=0, pady=5)
                root.grid_rowconfigure(0, weight=1)
                root.grid_columnconfigure(0, weight=1)
                self.text_area.grid(row=0, column=0, columnspan=2, sticky="nsew")

                self.root.protocol("WM_DELETE_WINDOW", self.close)
                self.update_text()

            def close(self):
                global debug_opened
                debug_opened = False
                self.root.destroy()

            def copy_text(self):
                self.text_area.tag_add("sel", "1.0", "end")
                self.text_area.focus_set()
                self.text_area.event_generate("<<Copy>>")
            def update_text(self):
                new_text = Debug.get_str()
                self.text_area.config(state="normal")
                self.text_area.delete("1.0", "end")
                self.text_area.insert("1.0", new_text)
                self.text_area.config(state="disabled")
                self.root.after(5000, self.update_text)
        if debug_opened:
            return
        debug = tk.Tk()
        DebugWindow(debug)


    def open_text_settings():
        def close_settings_window():
            global settings_text_open, settings_text_window
            settings_text_open = False
            settings_text_window.destroy()
        def guide():
            webbrowser.open("https://github.com/Soto4ka37/Yandex-Music-RPC-Lite/tree/master/assets/guide.md")
        def save():
            global lasttrack, lastradio, nowplaymode
            lasttrack = lastradio = nowplaymode = None
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
        settings_text_window.title("Редактор текста статуса")
        settings_text_open = True
        settings_text_window.protocol("WM_DELETE_WINDOW", close_settings_window)

        btn = Button(settings_text_window, text="Список переменных", command=guide, width=39)  
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
        global settings_open, settings_text_window, nowplaymode, settings_window
        if settings_open:
            return
        
        def on_button():
            global lasttrack, lastradio, nowplaymode
            lasttrack = lastradio = nowplaymode = None
            settings['t_button'] = button_var.get()
            save_settings(settings)

        def on_timewave():
            global lasttrack, lastradio, nowplaymode
            lasttrack = lastradio = nowplaymode = None
            settings['w_time'] = timewave_var.get()
            save_settings(settings)

        def on_clearnodata():
            global lasttrack, lastradio, nowplaymode
            lasttrack = lastradio = nowplaymode = None
            settings['n_clear'] = clearnodata_var.get()
            save_settings(settings)

        def on_timenodata():
            global lasttrack, lastradio, nowplaymode
            lasttrack = lastradio = nowplaymode = None
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
            global lasttrack, lastradio, nowplaymode
            lasttrack = lastradio = nowplaymode = None
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
        ping = Spinbox(settings_window, textvariable=pingvar, from_=1, to=3, width=8, command=on_ping)
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

        lbl = Label(settings_window, text="[Настройки применяются автоматически]", font=("Arial Bold", 12))
        lbl.grid(row=17, column=0, sticky="w")

    def update_status():    
        global lasttrack, lastradio, nowplaymode, lastclick, rpc, app_var
        lasttrack = lastradio = nowplaymode = None
        if app_var.get():
            now = time() 
            last = now - lastclick
            if last <= 10:
                app_var.set(False)
                if settings.get("image"):
                    change_image('https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Icon.png')
                name.set('Слишком много попыток!')
                author.set(f'Повторите попытку через {int((10 - last))} сек')
                return
            lastclick = time()
            name.set("Загрузка...")
            author.set('Подключение к Discord.')
            if settings.get("image"):
                change_image('https://music.yandex.ru/blocks/playlist-cover/playlist-cover_no_cover4.png')
            rpc = RPC()
            if not rpc.rpc:
                rpc = None
                if settings.get("image"):
                    change_image('https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Icon.png')
                name.set('Не удалось подключиться к дискорду')
                author.set('Дискорд не найден')
                app_var.set(False)
                settings['on'] = False
                save_settings(settings)
                return
            author.set('Ожидание ответа от API')
            settings["on"] = True
            save_settings(settings)
        else:
            settings["on"] = False
            try:
                rpc.disconnect()
            except:
                pass
            save_settings(settings)

    def change_image(url: str):
        response = requests.get(url)
        image_data = response.content

        image = Image.open(BytesIO(image_data))
        image = image.resize((75, 75))
        image = ImageTk.PhotoImage(image)

        image_label.config(image=image)
        image_label.photo = image

    def quit_window(icon, item):
        global mainloop
        settings['on'] = False
        mainloop = False
        show_window(icon, item)
        window.destroy()

    def show_settings(icon, item):
        show_window(icon, item)
        open_settings()

    def show_window(icon, item):
        global nowindow
        icon.stop()
        nowindow = False
        window.after(0,window.deiconify)

    def open_github_issues():
        webbrowser.open("https://github.com/Soto4ka37/Yandex-Music-RPC-Lite/issues")

    def open_github():
        webbrowser.open("https://github.com/Soto4ka37/Yandex-Music-RPC-Lite/")

    def withdraw_window():  
        global need_notify, icon, settings_window, settings_text_window, settings_open, nowindow, settings_text_open
        try:
            settings_text_window.destroy()
            settings_text_open = False
        except:
            pass
        try:
            settings_window.destroy()
            settings_open = False
        except:
            pass
        if settings.get('on', False) and settings.get('background'):
            name.set('Фоновый режим завершён')
            author.set('Данные обновятся при смене трека')
            if settings.get("image"):
                change_image('https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Icon.png')
            nowindow = True
            window.withdraw()
            image = Image.open(icon_path)
            menu = (pystray.MenuItem('Открыть', show_window, default=True), pystray.MenuItem('Настройки', show_settings), pystray.MenuItem('GitHub', open_github), pystray.MenuItem('Выход', quit_window))
            icon = pystray.Icon("name", image, f"RPC {version}", menu)
            need_notify = True
            icon.run()
        else:
            global mainloop
            window.destroy()
            settings['on'] = False
            mainloop = False
    window = tk.Tk()
    window.iconbitmap(icon_path)
    window.minsize(250, 90)
    window.title(f"RPC {version}")
    app_var = tk.BooleanVar(value=settings.get('on', False))
    app_checkbox = Checkbutton(window, text="Подключиться", variable=app_var, command=update_status)

    name = tk.StringVar()
    author = tk.StringVar()
    
    name_label = Label(window, textvariable=name)
    author_label = Label(window, textvariable=author)
    image_label = Label(window)

    update_status()
    change_image('https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Icon.png')

    menu = tk.Menu(window)  
    m = tk.Menu(menu, tearoff=0)  
    m.add_command(label='Базовые настройки', command=open_settings)  
    m.add_command(label='Редактор текста статуса', command=open_text_settings)  
    menu.add_cascade(label='Настройки', menu=m) 
    m = tk.Menu(menu, tearoff=0)  
    m.add_command(label='Откладка', command=open_debug)  
    m.add_command(label='Сообщить об ошибке', command=open_github_issues)  
    menu.add_cascade(label='Откладка', men=m) 
    window.config(menu=menu)  
    image_label.grid(row=0, column=0, rowspan=3, sticky="w", padx=5, pady=5)
    app_checkbox.grid(row=0, column=1, sticky="w", padx=5)
    name_label.grid(row=1, column=1, sticky="w", padx=5)
    author_label.grid(row=2, column=1, sticky="w", padx=5)
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
    global lasttrack, lastradio, nowplaymode, rpc, icon, need_notify, app_var
    lasttrack = lastradio = nowplaymode = None
    client = getclient()
    song = API(client)

    while mainloop:
        if need_notify:
            icon.notify(title='Скрыто в трей', message='Приложение работет в фоновом режиме')
            need_notify = False
        try:
            if rpc:
                if settings.get("on"):
                    song.update()
                    if song.fulldone:
                        if song.link != lasttrack:
                            lasttrack = song.link
                            nowplaymode = None

                        if nowplaymode not in (2, 1):
                            rpc.update(song, settings)
                            if settings.get('on'):
                                if not nowindow:
                                    details = rpc.param_to_text(settings.get('tr_details'), song)
                                    state = rpc.param_to_text(settings.get('tr_state'), song)
                                    name.set(details)
                                    author.set(state)
                                    if settings.get('image'):
                                        change_image(song.icon)
                            lastupdate = time()
                            nowplaymode = 1

                        elif settings.get('t_time') and nowplaymode != 2:
                            r_time = (time() - lastupdate)
                            if r_time >= song.total:
                                rpc.repeat(song, settings, lastupdate)
                                if not nowindow:
                                    details = rpc.param_to_text(settings.get('re_details'), song)
                                    state = rpc.param_to_text(settings.get('re_state'), song)
                                    name.set(details)
                                    author.set(state)
                                if settings.get('t_time', 2) == 1:
                                    lastupdate = time()
                                elif settings.get('t_time', 2) == 2:
                                    nowplaymode = 2

                    elif song.partdone and song.type and song.type == 'radio':
                            if song.description != lastradio:
                                rpc.song(song=song, settings=settings)
                                if settings.get('on'):
                                    if not nowindow:
                                        details = rpc.param_to_text(settings.get('ww_details'), song)
                                        state = rpc.param_to_text(settings.get('ww_state'), song)
                                        name.set(details)
                                        author.set(state)
                                        if settings.get('image'):
                                            change_image('https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Wave.png')
                                lastradio = song.description
                                nowplaymode = None
                    else:
                        if nowplaymode != 0:
                            rpc.nodata(settings)
                            nowplaymode = 0
                            if settings.get('on'):
                                if not nowindow:
                                    details = settings.get('no_details')
                                    state = settings.get('no_state')
                                    name.set(details)
                                    author.set(state)
                                    if settings.get('image'):
                                        change_image('https://music.yandex.ru/blocks/playlist-cover/playlist-cover_no_cover4.png')
                    sleep(settings.get('ping'))
                else:
                    rpc.clear()
                    lasttrack = lastradio = nowplaymode = None
                    sleep(settings.get('ping') + 2)
            else:
                sleep(settings.get('ping') + 2)
        except Exception as e:
            if 'Event loop is closed' in str(e) or 'The pipe was closed' in str(e):
                if settings.get("image"):
                    change_image('https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Icon.png')
                rpc = None
                app_var.set(False)
                name.set('Соединение с Discord разорвано')
                author.set('Пожалуйста переподключитесь')
                Debug.add(f'[ОШИБКА]\nСоединение с дискордом разорвано\n{e}')
            else:
                error = traceback.format_exc()
                error = f'[КРИТИЧЕСКАЯ ОШИБКА]\n{error}'
                Debug.add(error)
            sleep(2)

if __name__ == "__main__":
    t1 = Thread(target=presense)
    t1.start()
    
    t2 = Thread(target=gui)
    t2.start()
    
    t1.join()