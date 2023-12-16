import pystray
import webbrowser
import requests
import tkinter as tk
from tkinter.ttk import Button, Spinbox, Radiobutton, Checkbutton, Label, Entry, Scrollbar
from PIL import Image, ImageTk
from io import BytesIO
from time import time
import modules.debugger as debugger
from modules.data import save_settings, default, icon_path, version, settings
from modules.tempdata import opened_windows, params

def open_gui():
    def open_settings():
        if opened_windows.settings:
            return
        
        class SettingsWidnow:
            def __init__(self, root: tk.Toplevel):
                self.root = root
                root.title("Настройки")
                root.protocol("WM_DELETE_WINDOW", self.close)

                lbl = Label(root, text="Глобальные настройки", font=("Arial Bold", 17))
                n = 0

                lbl.grid(row=n, column=0, sticky="w")
                n += 1

                self.updatecheck_var = tk.BooleanVar(value=settings.get('update', True))
                updatecheck = Checkbutton(root, variable=self.updatecheck_var, text="Проверять обновления при запуске", command=self.on_updatecheck)
                updatecheck.grid(row=n, column=0, sticky="w")
                n += 1
                
                self.updateimage_var = tk.BooleanVar(value=settings.get('image', True))
                updateimage = Checkbutton(root, variable=self.updateimage_var, text="Обновлять картинку в приложении (Не влияет на статус)", command=self.on_updateimage)
                updateimage.grid(row=n, column=0, sticky="w")
                n += 1

                lbl = Label(root, text="Задержка между запросами (секунды)")
                lbl.grid(row=n, column=0, sticky="w")
                n += 1

                self.ping_var = tk.IntVar(value=settings.get('ping', 1))
                ping = Spinbox(root, textvariable=self.ping_var, from_=3, to=10, width=8, command=self.on_ping)
                ping.grid(row=n, column=0, sticky="w", padx=2)
                n += 1

                self.background_var = tk.BooleanVar(value=settings.get('background', False))
                background = Checkbutton(root, variable=self.background_var, text="Разрешить работу в фоновом режиме", command=self.on_background)
                background.grid(row=n, column=0, sticky="w")
                n += 1

                lbl = Label(root, text="Настройки статуса", font=("Arial Bold", 17))
                lbl.grid(row=n, column=0, sticky="w")
                n += 1

                lbl = Label(root, text="> Редакторы", font=("Arial Bold", 14))
                lbl.grid(row=n, column=0, sticky="w")
                n += 1
                
                btn = Button(root, text="Открыть редактор статуса", command=open_status_window)  
                btn.grid(row=n, column=0, sticky="ew")
                n += 1  

                self.button_var = tk.BooleanVar(value=settings.get('t_button', True))
                button = Checkbutton(root, variable=self.button_var, text='Включить кнопки', command=self.on_button)
                button.grid(row=n, column=0, sticky="w")
                n += 1

                btn = Button(root, text="Открыть редактор кнопок", command=open_button_window)  
                btn.grid(row=n, column=0, sticky="ew")
                n += 1  

                lbl = Label(root, text="> Трек и повтор", font=("Arial Bold", 14))
                lbl.grid(row=n, column=0, sticky="w")
                n += 1

                lbl = Label(root, text=">> Счётчик времени трека", font=("Arial Bold", 10))
                lbl.grid(row=n, column=0, sticky="w")
                n += 1

                self.time_rbvar = tk.IntVar(value=settings.get('t_time'))
                time_rb = Radiobutton(root, variable=self.time_rbvar, text='Выключить счётчик', value=0, command=self.on_timerb)  
                time_rb.grid(row=n, column=0, sticky="w")
                n += 1

                time_rb1 = Radiobutton(root, variable=self.time_rbvar, text='По окончании начинать "Осталось" с начала', value=1, command=self.on_timerb)  
                time_rb1.grid(row=n, column=0, sticky="w")
                n += 1

                time_rb2 = Radiobutton(root, variable=self.time_rbvar, text='По окончаннии менять "Осталось" на "Прошло"', value=2, command=self.on_timerb)  
                time_rb2.grid(row=n, column=0, sticky="w")
                n += 1

                lbl = Label(root, text="> Поток", font=("Arial Bold", 14))
                lbl.grid(row=n, column=0, sticky="w")
                n += 1

                self.timewave_var = tk.BooleanVar(value=settings.get('w_time', True))
                timewave = Checkbutton(root, variable=self.timewave_var, text="Считать время при прослушивании потока", command=self.on_timewave)
                timewave.grid(row=n, column=0, sticky="w")
                n += 1

                lbl = Label(root, text="> Неизвестный трек", font=("Arial Bold", 14))
                lbl.grid(row=n, column=0, sticky="w")
                n += 1
                
                self.clearnodata_var = tk.BooleanVar(value=settings.get('n_clear', False))
                clearnodata = Checkbutton(root, variable=self.clearnodata_var, text="Скрыть статус при неизвестном треке", command=self.on_clearnodata)
                clearnodata.grid(row=n, column=0, sticky="w")
                n += 1

                self.timenodata_var = tk.BooleanVar(value=settings.get('n_time', True))
                timenodata = Checkbutton(root, variable=self.timenodata_var, text="Считать время при неизвестном треке", command=self.on_timenodata)
                timenodata.grid(row=n, column=0, sticky="w")
                n += 1

                btn = Button(root, text="Полный сброс настроек", command=self.reset_settings)  
                btn.grid(row=n, column=0, sticky="ew")
                n += 1  
            def on_button(self):
                params.reloadStatus()
                settings['t_button'] = self.button_var.get()
                save_settings(settings)

            def on_timewave(self):
                params.reloadStatus()
                settings['w_time'] = self.timewave_var.get()
                save_settings(settings)

            def on_clearnodata(self):
                params.reloadStatus()
                settings['n_clear'] = self.clearnodata_var.get()
                save_settings(settings)

            def on_timenodata(self):
                params.reloadStatus()
                settings['n_time'] = self.timenodata_var.get()
                save_settings(settings)

            def on_ping(self):
                settings['ping'] = self.ping_var.get()
                save_settings(settings)

            def on_updatecheck(self):
                settings['update'] = self.updatecheck_var.get()
                save_settings(settings)

            def on_updateimage(self):
                settings['image'] = self.updateimage_var.get()
                save_settings(settings)

            def on_background(self):
                settings['background'] = self.background_var.get()
                save_settings(settings)

            def on_timerb(self):
                params.reloadStatus()
                t_time = self.time_rbvar.get()
                settings['t_time'] = t_time
                save_settings(settings)

            def close(self):
                opened_windows.settings = None
                self.root.destroy()

            def reset_settings(self):
                settings = default.copy()
                settings['on'] = False
                save_settings(settings)
                params.exit = True
                self.root.quit()

        setting_window = tk.Toplevel()
        setting_window = SettingsWidnow(setting_window)
        opened_windows.settings = setting_window

    def open_status_window():
        if opened_windows.status_editor:
            return
        class StatusWindow:
            def __init__(self, root: tk.Toplevel):
                self.root = root
                root.title("Редактор текста статуса")
                root.protocol("WM_DELETE_WINDOW", self.close)
                n = 0

                btn = Button(root, text="Список переменных", command=self.guide)  
                btn.grid(row=n, column=0, sticky="ew")  
                btn = Button(root, text="Применить", command=self.save)  
                btn.grid(row=n, column=1, sticky="ew")
                n += 1  

                lbl = Label(root, text="При треке", font=("Arial Bold", 15))
                lbl.grid(row=n, column=0, sticky="w")
                n += 1  

                lbl = Label(root, text="Верхняя строчка")
                lbl.grid(row=n, column=1, sticky="w")
                self.tr_details = tk.StringVar(value=settings.get('tr_details'))
                txt = Entry(root, textvariable=self.tr_details, width=40) 
                txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
                n += 1  

                lbl = Label(root, text="Нижняя строчка")
                lbl.grid(row=n, column=1, sticky="w")
                self.tr_state = tk.StringVar(value=settings.get('tr_state'))
                txt = Entry(root, textvariable=self.tr_state, width=40) 
                txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
                n += 1  

                lbl = Label(root, text="Большая картинка")
                lbl.grid(row=n, column=1, sticky="w")
                self.tr_large_image = tk.StringVar(value=settings.get('tr_large_image'))
                txt = Entry(root, textvariable=self.tr_large_image, width=40) 
                txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
                n += 1  

                lbl = Label(root, text="Маленькая картинка")
                lbl.grid(row=n, column=1, sticky="w")
                self.tr_small_image = tk.StringVar(value=settings.get('tr_small_image'))
                txt = Entry(root, textvariable=self.tr_small_image, width=40) 
                txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
                n += 1  

                lbl = Label(root, text="При повторе трека", font=("Arial Bold", 15))
                lbl.grid(row=n, column=0, sticky="w")
                n += 1  

                lbl = Label(root, text="Верхняя строчка")
                lbl.grid(row=n, column=1, sticky="w")
                self.re_details = tk.StringVar(value=settings.get('re_details'))
                txt = Entry(root, textvariable=self.re_details, width=40) 
                txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
                n += 1  

                lbl = Label(root, text="Нижняя строчка")
                lbl.grid(row=n, column=1, sticky="w")
                self.re_state = tk.StringVar(value=settings.get('re_state'))
                txt = Entry(root, textvariable=self.re_state, width=40) 
                txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
                n += 1  

                lbl = Label(root, text="Большая картинка")
                lbl.grid(row=n, column=1, sticky="w")
                self.re_large_image = tk.StringVar(value=settings.get('re_large_image'))
                txt = Entry(root, textvariable=self.re_large_image, width=40) 
                txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
                n += 1  

                lbl = Label(root, text="Маленькая картинка")
                lbl.grid(row=n, column=1, sticky="w")
                self.re_small_image = tk.StringVar(value=settings.get('re_small_image'))
                txt = Entry(root, textvariable=self.re_small_image, width=40) 
                txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
                n += 1  

                lbl = Label(root, text="При потоке", font=("Arial Bold", 15))
                lbl.grid(row=n, column=0, sticky="w")
                n += 1  

                lbl = Label(root, text="Верхняя строчка")
                lbl.grid(row=n, column=1, sticky="w")
                self.ww_details = tk.StringVar(value=settings.get('ww_details'))
                txt = Entry(root, textvariable=self.ww_details, width=40) 
                txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
                n += 1  

                lbl = Label(root, text="Нижняя строчка")
                lbl.grid(row=n, column=1, sticky="w")
                self.ww_state = tk.StringVar(value=settings.get('ww_state'))
                txt = Entry(root, textvariable=self.ww_state, width=40) 
                txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
                n += 1  

                lbl = Label(root, text="Большая картинка")
                lbl.grid(row=n, column=1, sticky="w")
                self.ww_large_image = tk.StringVar(value=settings.get('ww_large_image'))
                txt = Entry(root, textvariable=self.ww_large_image, width=40) 
                txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
                n += 1  

                lbl = Label(root, text="Маленькая картинка")
                lbl.grid(row=n, column=1, sticky="w")
                self.ww_small_image = tk.StringVar(value=settings.get('ww_small_image'))
                txt = Entry(root, textvariable=self.ww_small_image, width=40) 
                txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
                n += 1  

                lbl = Label(root, text="При неизвестном треке", font=("Arial Bold", 15))
                lbl.grid(row=n, column=0, sticky="w")
                n += 1  

                lbl = Label(root, text="Верхняя строчка")
                lbl.grid(row=n, column=1, sticky="w")
                self.no_details = tk.StringVar(value=settings.get('no_details'))
                txt = Entry(root, textvariable=self.no_details, width=40) 
                txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
                n += 1  

                lbl = Label(root, text="Нижняя строчка")
                lbl.grid(row=n, column=1, sticky="w")
                self.no_state = tk.StringVar(value=settings.get('no_state'))
                txt = Entry(root, textvariable=self.no_state, width=40) 
                txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
                n += 1  

                lbl = Label(root, text="Большая картинка")
                lbl.grid(row=n, column=1, sticky="w")
                self.no_large_image = tk.StringVar(value=settings.get('no_large_image'))
                txt = Entry(root, textvariable=self.no_large_image, width=40) 
                txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
                n += 1  
            def close(self):
                opened_windows.status_editor = None
                self.root.destroy()

            def guide(self):
                webbrowser.open("https://github.com/Soto4ka37/Yandex-Music-RPC-Lite/tree/master/assets/guide.md")
            def save(self):
                params.reloadStatus()
                settings['tr_details'] = self.tr_details.get()
                settings['tr_state'] = self.tr_state.get()
                settings['tr_large_image'] = self.tr_large_image.get()
                settings['tr_small_image'] = self.tr_small_image.get()
                settings['re_details'] = self.re_details.get()
                settings['re_state'] = self.re_state.get()
                settings['re_large_image'] = self.re_large_image.get()
                settings['re_small_image'] = self.re_small_image.get()
                settings['ww_details'] = self.ww_details.get()
                settings['ww_state'] = self.ww_state.get()
                settings['ww_large_image'] = self.ww_large_image.get()
                settings['ww_small_image'] = self.ww_small_image.get()
                settings['no_details'] = self.no_details.get()
                settings['no_state'] = self.no_state.get()
                settings['no_large_image'] = self.no_large_image.get()
                self.close()
        
        status_editor_window = tk.Toplevel()
        status_editor_window = StatusWindow(status_editor_window)
        opened_windows.status_editor = status_editor_window

    def open_button_window():
        if opened_windows.buttons_editor:
            return
        class ButtonEditor:
            def __init__(self, root: tk.Toplevel):
                self.root = root
                root.title("Редактор кнопок")
                root.protocol("WM_DELETE_WINDOW", self.close)
                n = 0

                btn = Button(root, text="Список переменных", command=self.guide)  
                btn.grid(row=n, column=0, sticky="ew")  
                btn = Button(root, text="Применить", command=self.save)  
                btn.grid(row=n, column=1, sticky="ew")
                n += 1  

                lbl = Label(root, text="Первая кнопка", font=("Arial Bold", 15))
                lbl.grid(row=n, column=0, sticky="ew")
                n += 1  

                self.b1_track_var = tk.BooleanVar(value=settings.get('b1_track', True))
                b1_track = Checkbutton(root, variable=self.b1_track_var, text="При треке")
                b1_track.grid(row=n, column=0, sticky="w")
                n += 1

                self.b1_repeat_var = tk.BooleanVar(value=settings.get('b1_repeat', True))
                b1_repeat = Checkbutton(root, variable=self.b1_repeat_var, text="При повторе трека")
                b1_repeat.grid(row=n, column=0, sticky="w")
                n += 1

                self.b1_wave_var = tk.BooleanVar(value=settings.get('b1_wave', False))
                b1_wave = Checkbutton(root, variable=self.b1_wave_var, text="При потоке")
                b1_wave.grid(row=n, column=0, sticky="w")
                n += 1

                self.b1_nodata_var = tk.BooleanVar(value=settings.get('b1_nodata', False))
                b1_nodata = Checkbutton(root, variable=self.b1_nodata_var, text="При неизвестном треке")
                b1_nodata.grid(row=n, column=0, sticky="w")
                n += 1

                lbl = Label(root, text="Текст")
                lbl.grid(row=n, column=1, sticky="w")
                self.first_button_label = tk.StringVar(value=settings.get('first_button_label', ''))
                txt = Entry(root, textvariable=self.first_button_label, width=40) 
                txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
                n += 1  

                lbl = Label(root, text="Ссылка")
                lbl.grid(row=n, column=1, sticky="w")
                self.first_button_url = tk.StringVar(value=settings.get('first_button_url', ''))
                txt = Entry(root, textvariable=self.first_button_url, width=40) 
                txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
                n += 1  

                lbl = Label(root, text="Вторая кнопка", font=("Arial Bold", 15))
                lbl.grid(row=n, column=0, sticky="w")
                n += 1

                self.b2_track_var = tk.BooleanVar(value=settings.get('b2_track', False))
                b2_track = Checkbutton(root, variable=self.b2_track_var, text="При треке")
                b2_track.grid(row=n, column=0, sticky="w")
                n += 1

                self.b2_repeat_var = tk.BooleanVar(value=settings.get('b2_repeat', False))
                b2_repeat = Checkbutton(root, variable=self.b2_repeat_var, text="При повторе трека")
                b2_repeat.grid(row=n, column=0, sticky="w")
                n += 1

                self.b2_wave_var = tk.BooleanVar(value=settings.get('b2_wave', False))
                b2_wave = Checkbutton(root, variable=self.b2_wave_var, text="При потоке")
                b2_wave.grid(row=n, column=0, sticky="w")
                n += 1

                self.b2_nodata_var = tk.BooleanVar(value=settings.get('b2_nodata', False))
                b2_nodata = Checkbutton(root, variable=self.b2_nodata_var, text="При неизвестном треке")
                b2_nodata.grid(row=n, column=0, sticky="w")
                n += 1

                lbl = Label(root, text="Текст")
                lbl.grid(row=n, column=1, sticky="w")
                self.second_button_label = tk.StringVar(value=settings.get('second_button_label', ''))
                txt = Entry(root, textvariable=self.second_button_label, width=40) 
                txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
                n += 1  

                lbl = Label(root, text="Ссылка")
                lbl.grid(row=n, column=1, sticky="w")
                self.second_button_url = tk.StringVar(value=settings.get('second_button_url', ''))
                txt = Entry(root, textvariable=self.second_button_url, width=40) 
                txt.grid(row=n, column=0, sticky="w", padx=2, pady=1)
                n += 1  

            def close(self):
                opened_windows.buttons_editor = None
                self.root.destroy()
            def guide(self):
                webbrowser.open("https://github.com/Soto4ka37/Yandex-Music-RPC-Lite/tree/master/assets/guide.md")
            def save(self):
                params.reloadStatus()
                settings['first_button_label'] = self.first_button_label.get()
                settings['first_button_url'] = self.first_button_url.get()
                settings['second_button_label'] = self.second_button_label.get()
                settings['second_button_url'] = self.second_button_url.get()
                settings['b1_track'] = self.b1_track_var.get()
                settings['b1_repeat'] = self.b1_repeat_var.get()
                settings['b1_wave'] = self.b1_wave_var.get()
                settings['b1_nodata'] = self.b1_nodata_var.get()
                settings['b2_track'] = self.b2_track_var.get()
                settings['b2_repeat'] = self.b2_repeat_var.get()
                settings['b2_wave'] = self.b2_wave_var.get()
                settings['b2_nodata'] = self.b2_nodata_var.get()
                save_settings(settings)
                self.close()

        button_editor_window = tk.Toplevel()
        button_editor_window = ButtonEditor(button_editor_window)
        opened_windows.buttons_editor = button_editor_window

    def open_debug_widnow():
        if opened_windows.debugger:
            return
        class DebugWindow:
            def __init__(self, root: tk.Toplevel):
                self.root = root
                self.root.title("Журнал отладки")
                self.root.minsize(330, 450)
                self.root.geometry('530x700')
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
                opened_windows.debugger = None
                self.root.destroy()

            def copy_text(self):
                self.text_area.tag_add("sel", "1.0", "end")
                self.text_area.focus_set()
                self.text_area.event_generate("<<Copy>>")

            def update_text(self):
                new_text = debugger.getString()
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
                    start_index = f"{i + 1}.0"
                    end_index = f"{i + 2}.0"
                    self.text_area.tag_add(f"bg_{i}", start_index, end_index)

                    if "[I]" in line:
                        self.text_area.tag_configure(f"bg_{i}", background="#30d5c8")
                    elif "[R]" in line:
                        self.text_area.tag_configure(f"bg_{i}", background="#65e665")
                    elif "[W]" in line:
                        self.text_area.tag_configure(f"bg_{i}", background="yellow")
                    else:
                        self.text_area.tag_configure(f"bg_{i}", background="#ff0033")
        debug_window = tk.Toplevel()
        debug_window = DebugWindow(debug_window)
        opened_windows.debugger = debug_window

    class MainWindow:
        def __init__(self, root: tk.Tk):
            self.root = root
            self.icon = None
            root.iconbitmap(icon_path)
            root.minsize(280, 90)
            root.title(f"RPC {version}")
            self.connected = tk.BooleanVar(value=settings.get('on', False))
            app_checkbox = Checkbutton(root, text="Подключиться", variable=self.connected, command=self.update_status)

            self.name = tk.StringVar()
            self.author = tk.StringVar()
            
            name_label = Label(root, textvariable=self.name)
            author_label = Label(root, textvariable=self.author)
            self.image_label = Label(root)

            self.update_status()
            self.editImage('https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Icon.png')

            menu = tk.Menu(root)  
            menu.add_cascade(label='Настройки', command=open_settings)  
            menu.add_cascade(label='Сообщить об ошибке', command=self.open_github_issues)  
            menu.add_cascade(label='Отладка', command=open_debug_widnow)  
            root.config(menu=menu) 

            self.image_label.grid(row=0, column=0, rowspan=3, sticky="w", padx=5, pady=5)
            app_checkbox.grid(row=0, column=1, sticky="w", padx=5)
            name_label.grid(row=1, column=1, sticky="w", padx=5)
            author_label.grid(row=2, column=1, sticky="w", padx=5)

            root.protocol("WM_DELETE_WINDOW", self.withdraw_window)
            root.bind("<Button-1>", self.on_drag_start)
            root.bind("<B1-Motion>", self.on_drag_motion)

        def on_drag_start(self, event: tk.Event):
            self.drag_data = {'x': event.x_root - self.root.winfo_x(), 'y': event.y_root - self.root.winfo_y()}

        def on_drag_motion(self, event: tk.Event):
            def move_window(event: tk.Event):
                self.root.geometry(f"+{event.x_root - self.drag_data['x']}+{event.y_root - self.drag_data['y']}")
            self.root.after(10, move_window, event)

        def editName(self, text: str = None):
            if text:
                self.name.set(text)
            else:
                self.name.set('')

        def editAuthor(self, text: str = None):
            if text:
                self.author.set(text)
            else:
                self.author.set('')

        def editConnect(self, status: bool):
            self.connected.set(status)

        def getConnect(self) -> bool:
            return self.connected.get()
        
        def update_status(self):    
            params.reloadStatus()
            if self.getConnect():
                now = time() 
                last = now - params.lastclick
                if last <= 10:
                    self.editConnect(False)
                    settings['on'] = False
                    if settings.get("image"):
                        self.editImage('https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Icon.png')
                    self.editName('Вы слишком часто переподключаетесь!')
                    self.editAuthor(f'Попробуйте снова через {int((10 - last))} сек')
                    save_settings(settings)
                    return
                
                params.lastclick = now

                self.editName("Загрузка...")
                self.editAuthor('Подключение к Discord.')
                if settings.get("image"):
                    self.editImage('https://music.yandex.ru/blocks/playlist-cover/playlist-cover_no_cover4.png')
                rpc = params.createRPC()
                if not rpc.success:
                    params.closeRPC()
                    params.reloadStatus()

                    self.editConnect(False)
                    settings['on'] = False
                    save_settings(settings)

                    
                    if settings.get("image"):
                        self.editImage('https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Icon.png')
                    self.editName('Не удалось подключиться к дискорду')
                    self.editAuthor(rpc.exception)
                    return
                
                self.editAuthor('Ожидание ответа от API')
                settings["on"] = True
                save_settings(settings)
            else:
                params.closeRPC()
                params.reloadStatus()
                settings["on"] = False
                self.editName()
                self.editAuthor()
                if settings.get("image"):
                    self.editImage('https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Icon.png')
                save_settings(settings)

        def editImage(self, url: str):
            response = requests.get(url, timeout=10)
            image_data = response.content

            image = Image.open(BytesIO(image_data))
            image = image.resize((75, 75))
            image = ImageTk.PhotoImage(image)

            self.image_label.config(image=image)
            self.image_label.photo = image

        def quit_window(self, icon, item):
            self.show_window(icon, item)
            settings['on'] = False
            params.exit = True
            self.root.quit()

        def show_settings(self, icon, item):
            self.show_window(icon, item)
            open_settings()

        def show_window(self, icon, item):
            icon.stop()
            self.icon = None
            opened_windows.main_hiden = False
            self.root.after(0, self.root.deiconify)

        def open_github_issues(self):
            webbrowser.open("https://github.com/Soto4ka37/Yandex-Music-RPC-Lite/issues")

        def open_github(self):
            webbrowser.open("https://github.com/Soto4ka37/Yandex-Music-RPC-Lite/")

        def withdraw_window(self):  
            debugger_widnow = opened_windows.debugger
            status_editor_window = opened_windows.status_editor
            button_editor_window = opened_windows.buttons_editor
            settings_window = opened_windows.settings

            if debugger_widnow:
                debugger_widnow.root.destroy()
                opened_windows.debugger = None
                
            if status_editor_window:
                status_editor_window.root.destroy()
                opened_windows.status_editor = None

            if button_editor_window:
                button_editor_window.root.destroy()
                opened_windows.buttons_editor = None

            if settings_window:
                settings_window.root.destroy()
                opened_windows.settings = None

            if settings.get('on', False) and settings.get('background'):
                opened_windows.main_hiden = True
                params.need_notify = True
                params.need_update_main_window = True
                self.editName('В фоновом режиме')
                self.editAuthor()
                if settings.get("image"):
                    self.editImage('https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Icon.png')

                self.root.withdraw()
                image = Image.open(icon_path)
                menu = (pystray.MenuItem('Открыть', self.show_window, default=True), pystray.MenuItem('GitHub', self.open_github), pystray.MenuItem('Выход', self.quit_window))
                self.icon = pystray.Icon("name", image, f"RPC {version}", menu)
                self.icon.run()
            else:
                settings['on'] = False
                params.exit = True
                opened_windows.main = None
                self.root.quit()

    main_window = tk.Tk()
    main_window = MainWindow(main_window)
    opened_windows.main = main_window
    main_window.root.mainloop()
