from modules.open_webpage import ask_open
import tkinter as tk
from tkinter.ttk import Button, Checkbutton, Label, Entry
from modules.data import save_settings, settings
from modules.tempdata import opened_windows, params
import ctypes

def check_en():
    u = ctypes.windll.LoadLibrary("user32.dll")
    pf = getattr(u, "GetKeyboardLayout")
    if hex(pf(0)) == '0x4090409':
        return True
    else:
        return False
    
class ButtonEditor:
    def __init__(self, root: tk.Toplevel):
        root.bind("<Key>", self.callback)
        self.root = root
        root.title("Редактор кнопок")
        root.protocol("WM_DELETE_WINDOW", self.close)
        n = 0

        btn = Button(root, text="Список переменных", command=self.guide)  
        btn.grid(row=n, column=0, sticky="ew")  
        btn = Button(root, text="Применить", command=self.save)  
        btn.grid(row=n, column=1, sticky="ew")
        n += 1  

        self.button_var = tk.BooleanVar(value=settings.get('t_button', True))
        obj = Checkbutton(root, variable=self.button_var, text='Включить кнопки', command=self.on_button)
        obj.grid(row=n, column=0, sticky="w", columnspan=3)
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

    # если это кто-то читает это просто знайте:  
    # ЕБУЧИЙ TKINTER НЕ ПОДДЕРЖИВАЕТ КОПИРОВАНИЕ И ВСТАВКУ НА ЛЮБЫХ ДРУГИХ РАСКЛАДКАХ ПОМИМО АНГИЙСКОГО
    # Я ЭТУ ХУЙНЮ ПЫТАЛСЯ ДВА ЧАСА РЕШИТЬ
        
    def callback(self, event):
        if (event.state & 4 > 0):
            if not check_en():
                print(chr(event.keycode))
                if chr(event.keycode) == "V":
                    try:
                        widget = event.widget
                        if widget.select_present():
                            widget.delete("sel.first", "sel.last")
                        text_to_paste = self.root.clipboard_get()
                        widget.insert(tk.INSERT, text_to_paste)
                    except:
                        pass
                elif chr(event.keycode) == "C":
                    try:
                        widget = event.widget
                        selected_text = widget.selection_get()
                        if selected_text:
                            self.root.clipboard_clear()
                            self.root.clipboard_append(selected_text)
                    except:
                        pass
                elif chr(event.keycode) == "X":
                    try:
                        widget = event.widget
                        selected_text = widget.selection_get()
                        if selected_text:
                            widget.delete("sel.first", "sel.last")
                            self.root.clipboard_clear()
                            self.root.clipboard_append(selected_text)
                    except:
                        pass

    def on_button(self):
        params.reloadStatus()
        settings['t_button'] = self.button_var.get()
        save_settings(settings)

    def close(self):
        opened_windows.buttons_editor = None
        self.root.destroy()

    def guide(self):
        ask_open("https://github.com/Soto4ka37/Yandex-Music-RPC-Lite/tree/master/assets/guide.md")
        
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

def run():
    if opened_windows.buttons_editor:
        return
    
    button_editor_window = tk.Toplevel()
    button_editor_window = ButtonEditor(button_editor_window)
    opened_windows.buttons_editor = button_editor_window