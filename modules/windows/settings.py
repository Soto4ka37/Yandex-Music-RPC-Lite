import tkinter as tk
from PIL import Image, ImageTk
from tkinter.ttk import Button, Checkbutton, Label, Frame, Notebook, Spinbox, Radiobutton
from tkinter import messagebox

from modules.data import old_image, new_image, none_image, settings
from modules.data import save_settings, default, settings
from modules.tempdata import opened_windows, params

from modules.windows.status import run as open_status_editor
from modules.windows.buttons import run as open_button_editor
from modules.windows.tooltip import ToolTip

class SettingsWidnow:
    def __init__(self, root: tk.Toplevel):
        self.root = root
        self.root.title("Настройки")
        root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.geometry("300x400")
        self.root.resizable(width=False, height=False)

        self.root.notebook = Notebook(self.root)
        self.root.notebook.pack()

        # ГЛОБАЛЬНЫЕ НАСТРОЙКИ
        n = 0
        frame = Frame(self.root.notebook)
        self.root.notebook.add(frame, text='Приложение')

        obj = Label(frame, text="Глобальные настройки", font=("Arial Bold", 18))
        obj.grid(row=n, column=0, columnspan=3)
        n += 1

        self.ping_var = tk.IntVar(value=settings.get('ping', 1))
        obj = Spinbox(frame, textvariable=self.ping_var, from_=3, to=10, width=5, command=self.on_ping)
        obj.grid(row=n, column=0, sticky="w", padx=2)
        lbl = Label(frame, text="Задержка между запросами в секундах (?)")
        self.pg_tooltip = ToolTip(obj, 'От 3 до 10')
        self.pglb_tooltip = ToolTip(lbl, 'Промежуток между запросами на сервера яндекса и обновлением статуса (Производетельность)')
        lbl.grid(row=n, column=1, sticky="w")
        n += 1

        self.updatecheck_var = tk.BooleanVar(value=settings.get('update', True))
        obj = Checkbutton(frame, variable=self.updatecheck_var, text="Проверять наличие обновлений", command=self.on_updatecheck)
        obj.grid(row=n, column=0, sticky="w", columnspan=3)
        n += 1
        
        self.updateimage_var = tk.BooleanVar(value=settings.get('image', True))
        obj = Checkbutton(frame, variable=self.updateimage_var, text="Предпросмотр иконки трека (?)", command=self.on_updateimage)
        obj.grid(row=n, column=0, sticky="w", columnspan=3)
        self.ic_tooltip = ToolTip(obj, 'Обновление изображения находящегося левее кнопки подключиться (Не влияет на статус)')
        n += 1

        self.background_var = tk.BooleanVar(value=settings.get('background', False))
        obj = Checkbutton(frame, variable=self.background_var, text="Разрешить фоновый режим (?)", command=self.on_background)
        obj.grid(row=n, column=0, sticky="w", columnspan=3)
        self.bk_tooltip = ToolTip(obj, 'При нажатии на кнопку "X" приложение будет минимизировано в системный трей вместо того, чтобы полностью закрыться')
        n += 1

        obj = Button(frame, text="Сброс настроек", command=self.reset_settings)  
        obj.grid(row=n, column=0, sticky="ew", columnspan=3, padx=3)
        n += 1  

        # НАСТРОЙКИ СТАТУСА
        frame = Frame(self.root.notebook)
        self.root.notebook.add(frame, text='Статус')
        n = 0

        obj = Label(frame, text="Настройки статуса", font=("Arial Bold", 18))
        obj.grid(row=n, column=0, columnspan=6)
        n += 1

        obj = Button(frame, text="Редактировать статус", command=open_status_editor)  
        obj.grid(row=n, column=0, sticky="ew", columnspan=3, padx=3)

        obj = Button(frame, text="Редактировать кнопки", command=open_button_editor)  
        obj.grid(row=n, column=3, sticky="ew", columnspan=3, padx=3)
        n += 1  

        obj = Label(frame, text="> Логотип <", font=("Arial Bold", 15))
        obj.grid(row=n, column=0, columnspan=6, pady=(10, 0))
        n += 1

        self.image_new = Image.open(new_image)
        self.image_new = self.image_new.resize((32, 32))
        self.image_new = ImageTk.PhotoImage(self.image_new)
        obj = Label(frame, image=self.image_new)
        obj.grid(row=n, column=0, columnspan=2, rowspan=2)

        self.image_old = Image.open(old_image)
        self.image_old = self.image_old.resize((32, 32))
        self.image_old = ImageTk.PhotoImage(self.image_old)
        obj = Label(frame, image=self.image_old)
        obj.grid(row=n, column=2, columnspan=2, rowspan=2)

        self.image_none = Image.open(none_image)
        self.image_none = self.image_none.resize((32, 32))
        self.image_none = ImageTk.PhotoImage(self.image_none)
        obj = Label(frame, image=self.image_none)
        obj.grid(row=n, column=4, columnspan=2, rowspan=2)
        n += 2

        self.icon = tk.StringVar(value=settings.get('icon'))
        obj = Radiobutton(frame, variable=self.icon, text='Новый', value='https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-New.png', command=self.on_icon)  
        obj.grid(row=n, column=0, columnspan=2)

        obj = Radiobutton(frame, variable=self.icon, text='Старый', value='https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Default.png', command=self.on_icon)  
        obj.grid(row=n, column=2, columnspan=2)

        obj = Radiobutton(frame, variable=self.icon, text='Скрыть', value='', command=self.on_icon)  
        obj.grid(row=n, column=4, columnspan=2)
        n += 1


        obj = Label(frame, text="> Основной счётчик времени < ", font=("Arial Bold", 15))
        obj.grid(row=n, column=0, columnspan=6, pady=(10, 0))
        n += 1

        self.time_rbvar = tk.IntVar(value=settings.get('t_time'))
        obj = Radiobutton(frame, variable=self.time_rbvar, text='Выкл', value=0, command=self.on_timerb)  
        obj.grid(row=n, column=0, columnspan=2)

        obj = Radiobutton(frame, variable=self.time_rbvar, text='Повтор (?)', value=1, command=self.on_timerb)  
        obj.grid(row=n, column=2, columnspan=2)
        self.povt_tooltip = ToolTip(obj, 'При завершении трека отсчет "Осталось" начинается с начала')

        obj = Radiobutton(frame, variable=self.time_rbvar, text='Умный (?)', value=2, command=self.on_timerb)  
        obj.grid(row=n, column=4, columnspan=2)
        self.sm_tooltip = ToolTip(obj, 'При завершении трека отсчёт "Осталось" меняется на "Прошло"')
        n += 1

        obj = Label(frame, text="> Поток <", font=("Arial Bold", 15))
        obj.grid(row=n, column=0, columnspan=6, pady=(10, 0))
        n += 1

        self.wave_animate_var = tk.BooleanVar(value=settings.get('wave_animated_icon', True))
        obj = Checkbutton(frame, variable=self.wave_animate_var, text="Анимированная иконка (?)", command=self.on_wave_animate)
        obj.grid(row=n, column=1, sticky="w", columnspan=5)
        self.an_tooltip = ToolTip(obj, 'Заменяет статическую (.png) иконку потока на анимированную (.gif)')
        n += 1

        self.timewave_var = tk.BooleanVar(value=settings.get('w_time', True))
        obj = Checkbutton(frame, variable=self.timewave_var, text="Счётчик времени", command=self.on_timewave)
        obj.grid(row=n, column=1, sticky="w", columnspan=5)
        n += 1

        obj = Label(frame, text="> Нет данных <", font=("Arial Bold", 15))
        obj.grid(row=n, column=0, columnspan=6, pady=(10, 0))
        n += 1
        
        self.clearnodata_var = tk.BooleanVar(value=settings.get('n_clear', False))
        obj = Checkbutton(frame, variable=self.clearnodata_var, text="Скрыть статус (?)", command=self.on_clearnodata)
        obj.grid(row=n, column=1, sticky="w", columnspan=5)
        self.un_tooltip = ToolTip(obj, 'Скрывать статус при отсутсвии информации о текущем треке')
        n += 1

        self.timenodata_var = tk.BooleanVar(value=settings.get('n_time', True))
        obj = Checkbutton(frame, variable=self.timenodata_var, text="Счётчик времени", command=self.on_timenodata)
        obj.grid(row=n, column=1, sticky="w", columnspan=5)
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

    def on_wave_animate(self):
        params.reloadStatus()
        value = self.wave_animate_var.get()
        settings['wave_animated_icon'] = value
        if value:
            settings['wave_icon'] = 'https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Wave.gif'
        else:
            settings['wave_icon'] = 'https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Wave.png'
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

    def on_icon(self):
        params.reloadStatus()
        icon = self.icon.get()
        if icon == '':
            icon = None
        settings['icon'] = icon
        save_settings(settings)

    def close(self):
        opened_windows.settings = None
        self.root.destroy()

    def reset_settings(self):
        answer = messagebox.askquestion("Подтверждение", "Вы действительно хотите сбросить настройки?")
        if answer == 'yes':
            settings = default.copy()
            settings['on'] = False
            save_settings(settings)
            opened_windows.close_all()

def run():
    if opened_windows.settings:
        root: tk.Toplevel = opened_windows.settings.root
        if root.state() == 'iconic':
            root.deiconify()
        elif root.state() == 'normal':
            root.focus_force()
        return
    
    setting_window = tk.Toplevel()
    setting_window = SettingsWidnow(setting_window)
    opened_windows.settings = setting_window