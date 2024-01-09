import tkinter as tk
from tkinter.ttk import Button, Spinbox, Radiobutton, Checkbutton, Label
from tkinter import messagebox
from modules.data import save_settings, default, settings
from modules.tempdata import opened_windows, params

from modules.windows.status import run as open_status_editor
from modules.windows.buttons import run as open_button_editor
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

        lbl = Label(root, text="> Иконка", font=("Arial Bold", 14))
        lbl.grid(row=n, column=0, sticky="w")
        n += 1

        self.icon = tk.StringVar(value=settings.get('icon'))
        iconB = Radiobutton(root, variable=self.icon, text='Новая иконка', value='https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-New.png', command=self.on_icon)  
        iconB.grid(row=n, column=0, sticky="w")
        n += 1

        iconB = Radiobutton(root, variable=self.icon, text='Старая иконка', value='https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Default.png', command=self.on_icon)  
        iconB.grid(row=n, column=0, sticky="w")
        n += 1

        iconB = Radiobutton(root, variable=self.icon, text='Скрыть иконку', value='', command=self.on_icon)  
        iconB.grid(row=n, column=0, sticky="w")
        n += 1

        lbl = Label(root, text="> Редакторы", font=("Arial Bold", 14))
        lbl.grid(row=n, column=0, sticky="w")
        n += 1
        
        btn = Button(root, text="Открыть редактор статуса", command=open_status_editor)  
        btn.grid(row=n, column=0, sticky="ew")
        n += 1  

        self.button_var = tk.BooleanVar(value=settings.get('t_button', True))
        button = Checkbutton(root, variable=self.button_var, text='Включить кнопки', command=self.on_button)
        button.grid(row=n, column=0, sticky="w")
        n += 1

        btn = Button(root, text="Открыть редактор кнопок", command=open_button_editor)  
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

        time_rb = Radiobutton(root, variable=self.time_rbvar, text='По окончании начинать "Осталось" с начала', value=1, command=self.on_timerb)  
        time_rb.grid(row=n, column=0, sticky="w")
        n += 1

        time_rb = Radiobutton(root, variable=self.time_rbvar, text='По окончаннии менять "Осталось" на "Прошло"', value=2, command=self.on_timerb)  
        time_rb.grid(row=n, column=0, sticky="w")
        n += 1

        lbl = Label(root, text="> Поток", font=("Arial Bold", 14))
        lbl.grid(row=n, column=0, sticky="w")
        n += 1

        self.wave_animate_var = tk.BooleanVar(value=settings.get('wave_animated_icon', True))
        wave_animate = Checkbutton(root, variable=self.wave_animate_var, text="Анимированная иконка", command=self.on_wave_animate)
        wave_animate.grid(row=n, column=0, sticky="w")
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

    def on_wave_animate(self):
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
        return
    
    setting_window = tk.Toplevel()
    setting_window = SettingsWidnow(setting_window)
    opened_windows.settings = setting_window