version = "v8.3.1"
from time import sleep, time
import traceback
import os
from threading import Thread
import pystray
import webbrowser
import requests
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Button, Spinbox, Radiobutton, Checkbutton, Label, Entry, Scrollbar
from PIL import Image, ImageTk
from io import BytesIO

import modules.debugger as debugger
from modules.data import save_settings, load_settings, get_icon, default, icon_path 
from modules.api import getclient, API
from modules.presense import RPC
from modules.update import check_updates

mainloop = True # Флаг основного цикла
main_window_opened = settings_opened = status_editor_opened = debug_opened = button_editor_opened = False # Состояния окон
need_notify = False # Уведомление о сокрытии в трей
rpc = None # Объект статуса дискорда (Создаётся при подключении через интерфейс)
lastclick = 0 

client = getclient()
settings = load_settings()


if not os.path.exists(icon_path):
    get_icon()

if settings.get('update'):
    check_updates(version)

def gui():
    '''
    Интерфейс
    '''
    global name, author, change_image, show_window, app_var
    def resetstatusdata():
        '''Очищает состояние основного цикла и перезагружает статус'''
        global lasttrack, lastradio, nowplaymode
        lasttrack = lastradio = nowplaymode = None
    def open_debug():
        global deb_window
        class DebugWindow:
            def __init__(self, root: tk.Tk):
                global debug_opened
                debug_opened = True
                self.root = root
                self.root.title("Журнал отладки (Debug)")

                self.text_area = tk.Text(root, wrap="word", state="normal", height=25, width=40)
                initial_text = debugger.getString()
                self.text_area.insert("0.9", initial_text)
                self.text_area.config(state="disabled")

                scroll_y = Scrollbar(root, orient="vertical", command=self.text_area.yview)
                scroll_y.grid(row=0, column=1, sticky="nsew")
                self.text_area.config(yscrollcommand=scroll_y.set)

                menu = tk.Menu(root)  
                menu.add_cascade(label='Копировать', command=self.copy_text)  
                menu.add_cascade(label='Обновить', command=self.update_text)  
                root.config(menu=menu) 

                root.grid_rowconfigure(0, weight=1)
                root.grid_columnconfigure(0, weight=1)
                self.text_area.grid(row=0, column=0, columnspan=2, sticky="nsew")

                self.text_area.tag_configure("info", foreground="blue")
                self.text_area.tag_configure("request", foreground="green")
                self.text_area.tag_configure("warning", foreground="yellow")
                self.text_area.tag_configure("error", foreground="red")

                self.root.protocol("WM_DELETE_WINDOW", self.close)
                self.autoupdate_text_run()

            def close(self):
                global debug_opened
                debug_opened = False
                self.root.destroy()

            def copy_text(self):
                self.text_area.tag_add("sel", "1.0", "end")
                self.text_area.focus_set()
                self.text_area.event_generate("<<Copy>>")

            def update_text(self):
                new_text = debugger.getString()
                if self.text_area.get("1.0", "end") != new_text:
                    self.text_area.config(state="normal")
                    self.text_area.delete("1.0", "end")
                    self.text_area.insert("1.0", new_text)

                    self.apply_background()

                    self.text_area.config(state="disabled")

            def autoupdate_text_run(self):
                self.update_text()
                self.root.after(60000, self.autoupdate_text_run)

            def apply_background(self):
                content = self.text_area.get("1.0", "end-1c").splitlines()

                for i, line in enumerate(content):
                    if "[I]" in line:
                        self.text_area.tag_add(f"bg_{i}", f"{i + 1}.0", f"{i + 1}.end")
                        self.text_area.tag_configure(f"bg_{i}", background="#30d5c8")
                    elif "[R]" in line:
                        self.text_area.tag_add(f"bg_{i}", f"{i + 1}.0", f"{i + 1}.end")
                        self.text_area.tag_configure(f"bg_{i}", background="#65e665")
                    elif "[W]" in line:
                        self.text_area.tag_add(f"bg_{i}", f"{i + 1}.0", f"{i + 1}.end")
                        self.text_area.tag_configure(f"bg_{i}", background="yellow")
                    else:
                        self.text_area.tag_add(f"bg_{i}", f"{i + 1}.0", f"{i + 1}.end")
                        self.text_area.tag_configure(f"bg_{i}", background="#ff0033")

        if debug_opened:
            return
        debug = tk.Tk()
        deb_window = DebugWindow(debug)

    def open_status_window():
        def close_settings_window():
            global status_editor_opened, settings_text_window
            status_editor_opened = False
            settings_text_window.destroy()
        def guide():
            webbrowser.open("https://github.com/Soto4ka37/Yandex-Music-RPC-Lite/tree/master/assets/guide.md")
        def save():
            resetstatusdata()
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
        global status_editor_opened, settings_text_window
        if status_editor_opened:
            return
        
        settings_text_window = tk.Toplevel(window)
        settings_text_window.title("Редактор текста статуса")
        status_editor_opened = True
        settings_text_window.protocol("WM_DELETE_WINDOW", close_settings_window)
        n = 0

        btn = Button(settings_text_window, text="Список переменных", command=guide, width=39)  
        btn.grid(row=n, column=0)  
        btn = Button(settings_text_window, text="Применить", command=save, width=17)  
        btn.grid(row=n, column=1, sticky="w")
        n += 1  

        lbl = Label(settings_text_window, text="При треке", font=("Arial Bold", 15))
        lbl.grid(row=n, column=0, sticky="w")
        n += 1  

        lbl = Label(settings_text_window, text="Верхняя строчка")
        lbl.grid(row=n, column=1, sticky="w")
        tr_details = tk.StringVar()
        tr_details.set(settings.get('tr_details'))
        txt = Entry(settings_text_window, textvariable=tr_details, width=40) 
        txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
        n += 1  

        lbl = Label(settings_text_window, text="Нижняя строчка")
        lbl.grid(row=n, column=1, sticky="w")
        tr_state = tk.StringVar()
        tr_state.set(settings.get('tr_state'))
        txt = Entry(settings_text_window, textvariable=tr_state, width=40) 
        txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
        n += 1  

        lbl = Label(settings_text_window, text="Большая картинка")
        lbl.grid(row=n, column=1, sticky="w")
        tr_large_image = tk.StringVar()
        tr_large_image.set(settings.get('tr_large_image'))
        txt = Entry(settings_text_window, textvariable=tr_large_image, width=40) 
        txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
        n += 1  

        lbl = Label(settings_text_window, text="Маленькая картинка")
        lbl.grid(row=n, column=1, sticky="w")
        tr_small_image = tk.StringVar()
        tr_small_image.set(settings.get('tr_small_image'))
        txt = Entry(settings_text_window, textvariable=tr_small_image, width=40) 
        txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
        n += 1  

        lbl = Label(settings_text_window, text="При повторе трека", font=("Arial Bold", 15))
        lbl.grid(row=n, column=0, sticky="w")
        n += 1  

        lbl = Label(settings_text_window, text="Верхняя строчка")
        lbl.grid(row=n, column=1, sticky="w")
        re_details = tk.StringVar()
        re_details.set(settings.get('re_details'))
        txt = Entry(settings_text_window, textvariable=re_details, width=40) 
        txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
        n += 1  

        lbl = Label(settings_text_window, text="Нижняя строчка")
        lbl.grid(row=n, column=1, sticky="w")
        re_state = tk.StringVar()
        re_state.set(settings.get('re_state'))
        txt = Entry(settings_text_window, textvariable=re_state, width=40) 
        txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
        n += 1  

        lbl = Label(settings_text_window, text="Большая картинка")
        lbl.grid(row=n, column=1, sticky="w")
        re_large_image = tk.StringVar()
        re_large_image.set(settings.get('re_large_image'))
        txt = Entry(settings_text_window, textvariable=re_large_image, width=40) 
        txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
        n += 1  

        lbl = Label(settings_text_window, text="Маленькая картинка")
        lbl.grid(row=n, column=1, sticky="w")
        re_small_image = tk.StringVar()
        re_small_image.set(settings.get('re_small_image'))
        txt = Entry(settings_text_window, textvariable=re_small_image, width=40) 
        txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
        n += 1  

        lbl = Label(settings_text_window, text="При потоке", font=("Arial Bold", 15))
        lbl.grid(row=n, column=0, sticky="w")
        n += 1  

        lbl = Label(settings_text_window, text="Верхняя строчка")
        lbl.grid(row=n, column=1, sticky="w")
        ww_details = tk.StringVar()
        ww_details.set(settings.get('ww_details'))
        txt = Entry(settings_text_window, textvariable=ww_details, width=40) 
        txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
        n += 1  

        lbl = Label(settings_text_window, text="Нижняя строчка")
        lbl.grid(row=n, column=1, sticky="w")
        ww_state = tk.StringVar()
        ww_state.set(settings.get('ww_state'))
        txt = Entry(settings_text_window, textvariable=ww_state, width=40) 
        txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
        n += 1  

        lbl = Label(settings_text_window, text="Большая картинка")
        lbl.grid(row=n, column=1, sticky="w")
        ww_large_image = tk.StringVar()
        ww_large_image.set(settings.get('ww_large_image'))
        txt = Entry(settings_text_window, textvariable=ww_large_image, width=40) 
        txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
        n += 1  

        lbl = Label(settings_text_window, text="Маленькая картинка")
        lbl.grid(row=n, column=1, sticky="w")
        ww_small_image = tk.StringVar()
        ww_small_image.set(settings.get('ww_small_image'))
        txt = Entry(settings_text_window, textvariable=ww_small_image, width=40) 
        txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
        n += 1  

        lbl = Label(settings_text_window, text="При неизвестном треке", font=("Arial Bold", 15))
        lbl.grid(row=n, column=0, sticky="w")
        n += 1  

        lbl = Label(settings_text_window, text="Верхняя строчка")
        lbl.grid(row=n, column=1, sticky="w")
        no_details = tk.StringVar()
        no_details.set(settings.get('no_details'))
        txt = Entry(settings_text_window, textvariable=no_details, width=40) 
        txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
        n += 1  

        lbl = Label(settings_text_window, text="Нижняя строчка")
        lbl.grid(row=n, column=1, sticky="w")
        no_state = tk.StringVar()
        no_state.set(settings.get('no_state'))
        txt = Entry(settings_text_window, textvariable=no_state, width=40) 
        txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
        n += 1  

        lbl = Label(settings_text_window, text="Большая картинка")
        lbl.grid(row=n, column=1, sticky="w")
        no_large_image = tk.StringVar()
        no_large_image.set(settings.get('no_large_image'))
        txt = Entry(settings_text_window, textvariable=no_large_image, width=40) 
        txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
        n += 1  
    def open_button_window():
        def close_button_window():
            global button_editor_opened, button_window
            button_editor_opened = False
            button_window.destroy()
        def guide():
            webbrowser.open("https://github.com/Soto4ka37/Yandex-Music-RPC-Lite/tree/master/assets/guide.md")
        def save():
            resetstatusdata()
            settings['first_button_label'] = first_button_label.get()
            settings['first_button_url'] = first_button_url.get()
            settings['second_button_label'] = second_button_label.get()
            settings['second_button_url'] = second_button_url.get()
            settings['b1_track'] = b1_track_var.get()
            settings['b1_repeat'] = b1_repeat_var.get()
            settings['b1_wave'] = b1_wave_var.get()
            settings['b1_nodata'] = b1_nodata_var.get()
            settings['b2_track'] = b2_track_var.get()
            settings['b2_repeat'] = b2_repeat_var.get()
            settings['b2_wave'] = b2_wave_var.get()
            settings['b2_nodata'] = b2_nodata_var.get()
            save_settings(settings)
        global button_editor_opened, button_window
        if button_editor_opened:
            return
        button_window = tk.Toplevel(window)
        button_window.title("Редактор кнопок")
        button_editor_opened = True
        button_window.protocol("WM_DELETE_WINDOW", close_button_window)
        n = 0

        btn = Button(button_window, text="Список переменных", command=guide, width=39)  
        btn.grid(row=n, column=0)  
        btn = Button(button_window, text="Применить", command=save, width=17)  
        btn.grid(row=n, column=1, sticky="w")
        n += 1  

        lbl = Label(button_window, text="Первая кнопка", font=("Arial Bold", 15))
        lbl.grid(row=n, column=0, sticky="w")
        n += 1  

        b1_track_var = tk.BooleanVar(value=settings.get('b1_track', True))
        b1_track = Checkbutton(button_window, variable=b1_track_var, text="При треке")
        b1_track.grid(row=n, column=0, sticky="w")
        n += 1

        b1_repeat_var = tk.BooleanVar(value=settings.get('b1_repeat', True))
        b1_repeat = Checkbutton(button_window, variable=b1_repeat_var, text="При повторе трека")
        b1_repeat.grid(row=n, column=0, sticky="w")
        n += 1

        b1_wave_var = tk.BooleanVar(value=settings.get('b1_wave', False))
        b1_wave = Checkbutton(button_window, variable=b1_wave_var, text="При потоке")
        b1_wave.grid(row=n, column=0, sticky="w")
        n += 1

        b1_nodata_var = tk.BooleanVar(value=settings.get('b1_nodata', False))
        b1_nodata = Checkbutton(button_window, variable=b1_nodata_var, text="При неизвестном треке")
        b1_nodata.grid(row=n, column=0, sticky="w")
        n += 1

        lbl = Label(button_window, text="Текст")
        lbl.grid(row=n, column=1, sticky="w")
        first_button_label = tk.StringVar()
        first_button_label.set(settings.get('first_button_label', ''))
        txt = Entry(button_window, textvariable=first_button_label, width=40) 
        txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
        n += 1  

        lbl = Label(button_window, text="Ссылка")
        lbl.grid(row=n, column=1, sticky="w")
        first_button_url = tk.StringVar()
        first_button_url.set(settings.get('first_button_url', ''))
        txt = Entry(button_window, textvariable=first_button_url, width=40) 
        txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
        n += 1  

        lbl = Label(button_window, text="Вторая кнопка", font=("Arial Bold", 15))
        lbl.grid(row=n, column=0, sticky="w")
        n += 1

        b2_track_var = tk.BooleanVar(value=settings.get('b2_track', False))
        b2_track = Checkbutton(button_window, variable=b2_track_var, text="При треке")
        b2_track.grid(row=n, column=0, sticky="w")
        n += 1

        b2_repeat_var = tk.BooleanVar(value=settings.get('b2_repeat', False))
        b2_repeat = Checkbutton(button_window, variable=b2_repeat_var, text="При повторе трека")
        b2_repeat.grid(row=n, column=0, sticky="w")
        n += 1

        b2_wave_var = tk.BooleanVar(value=settings.get('b2_wave', False))
        b2_wave = Checkbutton(button_window, variable=b2_wave_var, text="При потоке")
        b2_wave.grid(row=n, column=0, sticky="w")
        n += 1

        b2_nodata_var = tk.BooleanVar(value=settings.get('b2_nodata', False))
        b2_nodata = Checkbutton(button_window, variable=b2_nodata_var, text="При неизвестном треке")
        b2_nodata.grid(row=n, column=0, sticky="w")
        n += 1

        lbl = Label(button_window, text="Текст")
        lbl.grid(row=n, column=1, sticky="w")
        second_button_label = tk.StringVar()
        second_button_label.set(settings.get('second_button_label', ''))
        txt = Entry(button_window, textvariable=second_button_label, width=40) 
        txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
        n += 1  

        lbl = Label(button_window, text="Ссылка")
        lbl.grid(row=n, column=1, sticky="w")
        second_button_url = tk.StringVar()
        second_button_url.set(settings.get('second_button_url', ''))
        txt = Entry(button_window, textvariable=second_button_url, width=40) 
        txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
        n += 1  

    def open_settings():
        global settings_opened, settings_text_window, nowplaymode, settings_window
        if settings_opened:
            return
        
        def on_button():
            resetstatusdata()
            settings['t_button'] = button_var.get()
            save_settings(settings)

        def on_timewave():
            resetstatusdata()
            settings['w_time'] = timewave_var.get()
            save_settings(settings)

        def on_clearnodata():
            resetstatusdata()
            settings['n_clear'] = clearnodata_var.get()
            save_settings(settings)

        def on_timenodata():
            resetstatusdata()
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
            resetstatusdata()
            t_time = time_rbvar.get()
            settings['t_time'] = t_time
            save_settings(settings)

        def close_settings_window():
            global settings_opened
            settings_opened = False
            settings_window.destroy()
        def reset_settings():
            global mainloop
            settings = default.copy()
            settings['on'] = False
            save_settings(settings)
            mainloop = False
            window.quit()
        settings_window = tk.Toplevel(window)
        settings_window.title("Настройки")
        settings_opened = True
        settings_window.protocol("WM_DELETE_WINDOW", close_settings_window)
        lbl = Label(settings_window, text="Глобальные настройки", font=("Arial Bold", 17))
        n = 0
        lbl.grid(row=n, column=0, sticky="w")
        n += 1

        updatecheck_var = tk.BooleanVar(value=settings.get('update', True))
        updatecheck = Checkbutton(settings_window, variable=updatecheck_var, text="Проверять обновления при запуске", command=on_updatecheck)
        updatecheck.grid(row=n, column=0, sticky="w")
        n += 1

        updateimage_var = tk.BooleanVar(value=settings.get('image', True))
        updateimage = Checkbutton(settings_window, variable=updateimage_var, text="Обновлять картинку в приложении (Не влияет на статус)", command=on_updateimage)
        updateimage.grid(row=n, column=0, sticky="w")
        n += 1

        lbl = Label(settings_window, text="Задержка между запросами (секунды)")
        lbl.grid(row=n, column=0, sticky="w")
        n += 1

        pingvar = tk.IntVar()
        pingvar.set(settings.get('ping', 1))
        ping = Spinbox(settings_window, textvariable=pingvar, from_=5, to=10, width=8, command=on_ping)
        ping.grid(row=n, column=0, sticky="w", padx=2)
        n += 1

        background_var = tk.BooleanVar(value=settings.get('background', False))
        background = Checkbutton(settings_window, variable=background_var, text="Разрешить работу в фоновом режиме", command=on_background)
        background.grid(row=n, column=0, sticky="w")
        n += 1

        lbl = Label(settings_window, text="Настройки статуса", font=("Arial Bold", 17))
        lbl.grid(row=n, column=0, sticky="w")
        n += 1

        lbl = Label(settings_window, text="> Редакторы", font=("Arial Bold", 14))
        lbl.grid(row=n, column=0, sticky="w")
        n += 1
        
        btn = Button(settings_window, text="Открыть редактор статуса", command=open_status_window, width=40)  
        btn.grid(row=n, column=0, sticky="w")
        n += 1  

        button_var = tk.BooleanVar(value=settings.get('t_button', True))
        button = Checkbutton(settings_window, variable=button_var, text='Включить кнопки', command=on_button)
        button.grid(row=n, column=0, sticky="w")
        n += 1

        btn = Button(settings_window, text="Открыть редактор кнопок", command=open_button_window, width=40)  
        btn.grid(row=n, column=0, sticky="w")
        n += 1  

        lbl = Label(settings_window, text="> Трек и повтор", font=("Arial Bold", 14))
        lbl.grid(row=n, column=0, sticky="w")
        n += 1

        lbl = Label(settings_window, text=">> Счётчик времени трека", font=("Arial Bold", 10))
        lbl.grid(row=n, column=0, sticky="w")
        n += 1

        time_rbvar = tk.IntVar()
        time_rbvar.set(settings.get('t_time'))
        time_rb = Radiobutton(settings_window, variable=time_rbvar, text='Выключить счётчик', value=0, command=on_timerb)  
        time_rb.grid(row=n, column=0, sticky="w")
        n += 1

        time_rb1 = Radiobutton(settings_window, variable=time_rbvar, text='По окончании начинать "Осталось" с начала', value=1, command=on_timerb)  
        time_rb1.grid(row=n, column=0, sticky="w")
        n += 1

        time_rb2 = Radiobutton(settings_window, variable=time_rbvar, text='По окончаннии менять "Осталось" на "Прошло"', value=2, command=on_timerb)  
        time_rb2.grid(row=n, column=0, sticky="w")
        n += 1

        lbl = Label(settings_window, text="> Поток", font=("Arial Bold", 14))
        lbl.grid(row=n, column=0, sticky="w")
        n += 1

        timewave_var = tk.BooleanVar(value=settings.get('w_time', True))
        timewave = Checkbutton(settings_window, variable=timewave_var, text="Считать время при прослушивании потока", command=on_timewave)
        timewave.grid(row=n, column=0, sticky="w")
        n += 1

        lbl = Label(settings_window, text="> Неизвестный трек", font=("Arial Bold", 14))
        lbl.grid(row=n, column=0, sticky="w")
        n += 1
        
        clearnodata_var = tk.BooleanVar(value=settings.get('n_clear', False))
        clearnodata = Checkbutton(settings_window, variable=clearnodata_var, text="Скрыть статус при неизвестном треке", command=on_clearnodata)
        clearnodata.grid(row=n, column=0, sticky="w")
        n += 1

        timenodata_var = tk.BooleanVar(value=settings.get('n_time', True))
        timenodata = Checkbutton(settings_window, variable=timenodata_var, text="Считать время при неизвестном треке", command=on_timenodata)
        timenodata.grid(row=n, column=0, sticky="w")
        n += 1

        lbl = Label(settings_window, text="*Эти настройки применяются автоматически", font=("Arial Bold", 12, "italic"))
        lbl.grid(row=n, column=0, sticky="w")
        n += 1

        btn = Button(settings_window, text="Полный сброс настроек", command=reset_settings, width=40)  
        btn.grid(row=n, column=0, sticky="w")
        n += 1  

    def update_status():    
        global lasttrack, lastradio, nowplaymode, lastclick, rpc, app_var
        resetstatusdata()
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
        show_window(icon, item)
        settings['on'] = False
        mainloop = False
        window.quit()

    def show_settings(icon, item):
        show_window(icon, item)
        open_settings()

    def show_window(icon, item):
        global main_window_opened
        icon.stop()
        main_window_opened = False
        window.after(0,window.deiconify)

    def open_github_issues():
        webbrowser.open("https://github.com/Soto4ka37/Yandex-Music-RPC-Lite/issues")

    def open_github():
        webbrowser.open("https://github.com/Soto4ka37/Yandex-Music-RPC-Lite/")

    def withdraw_window():  
        global need_notify, icon, settings_opened, main_window_opened, status_editor_opened, button_editor_opened, debug_opened
        if status_editor_opened:
            settings_text_window.destroy()
            status_editor_opened = False
        if settings_opened:
            settings_window.destroy()
            settings_opened = False
        if debug_opened:
            deb_window.root.destroy()
            debug_opened = False
        if button_editor_opened:
            button_window.destroy()
            button_editor_opened = False
        if settings.get('on', False) and settings.get('background'):
            name.set('Фоновый режим завершён')
            author.set('Данные обновятся при смене трека')
            if settings.get("image"):
                change_image('https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Icon.png')
            main_window_opened = True
            window.withdraw()
            image = Image.open(icon_path)
            menu = (pystray.MenuItem('Открыть', show_window, default=True), pystray.MenuItem('Настройки', show_settings), pystray.MenuItem('GitHub', open_github), pystray.MenuItem('Выход', quit_window))
            icon = pystray.Icon("name", image, f"RPC {version}", menu)
            need_notify = True
            icon.run()
        else:
            global mainloop
            settings['on'] = False
            mainloop = False
            window.quit()

    window = tk.Tk()
    window.iconbitmap(icon_path)
    window.minsize(270, 90)
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
    menu.add_cascade(label='Настройки', command=open_settings)  
    menu.add_cascade(label='Сообщить об ошибке', command=open_github_issues)  
    menu.add_cascade(label='Debug', command=open_debug)  
    window.config(menu=menu) 

    image_label.grid(row=0, column=0, rowspan=3, sticky="w", padx=5, pady=5)
    app_checkbox.grid(row=0, column=1, sticky="w", padx=5)
    name_label.grid(row=1, column=1, sticky="w", padx=5)
    author_label.grid(row=2, column=1, sticky="w", padx=5)
    def on_drag_start(event: tk.Event):
        global drag_data
        drag_data = {'x': event.x_root - window.winfo_x(), 'y': event.y_root - window.winfo_y()}

    def on_drag_motion(event: tk.Event):
        def move_window(event: tk.Event):
            window.geometry(f"+{event.x_root - drag_data['x']}+{event.y_root - drag_data['y']}")
        window.after(10, move_window, event)


    window.protocol("WM_DELETE_WINDOW", withdraw_window)
    window.bind("<Button-1>", on_drag_start)
    window.bind("<B1-Motion>", on_drag_motion)
    window.mainloop()

def presense():
    global lasttrack, lastradio, nowplaymode, rpc, icon, need_notify, app_var
    lasttrack = lastradio = nowplaymode = None
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
                                if not main_window_opened:
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
                                if not main_window_opened:
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
                                rpc.wave(song=song, settings=settings)
                                if settings.get('on'):
                                    if not main_window_opened:
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
                            rpc.nodata(settings, song)
                            nowplaymode = 0
                            if settings.get('on'):
                                if not main_window_opened:
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
                debugger.addWarning(f'Потеряна связь с дискордом: {e}')
            else:
                error = traceback.format_exc()
                name.set('Критическая ошибка')
                author.set('')
                app_var.set(False)
                rpc = None
                if settings.get("image"):
                    change_image('https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Icon.png')
                debugger.addError(f'Непредвиденное исключение\n{error}')
                messagebox.showerror('Yandex Music RPC | Непредвиденное исключение', message=f'{error}')

if __name__ == "__main__":
    t1 = Thread(target=presense)
    t1.start()
    
    t2 = Thread(target=gui)
    t2.start()
    
    t1.join()