from modules.open_webpage import ask_open
import tkinter as tk
from tkinter.ttk import Button, Label, Entry
from modules.data import settings
from modules.tempdata import opened_windows, params
import ctypes

def check_en():
    u = ctypes.windll.LoadLibrary("user32.dll")
    pf = getattr(u, "GetKeyboardLayout")
    if hex(pf(0)) == '0x4090409':
        return True
    else:
        return False
    
class StatusEditor:
    def __init__(self, root: tk.Toplevel):
        root.bind("<Key>", self.callback)
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

    def close(self):
        opened_windows.status_editor = None
        self.root.destroy()

    def guide(self):
        ask_open("https://github.com/Soto4ka37/Yandex-Music-RPC-Lite/tree/master/assets/guide.md")

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
        
def run():
    if opened_windows.status_editor:
        return
    
    status_editor_window = tk.Toplevel()
    status_editor_window = StatusEditor(status_editor_window)
    opened_windows.status_editor = status_editor_window