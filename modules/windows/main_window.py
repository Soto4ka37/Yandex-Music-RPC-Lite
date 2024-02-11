import pystray
import ctypes
import requests
from ttkthemes import ThemedTk
import tkinter as tk
from tkinter.ttk import Checkbutton, Label, Button
from PIL import Image, ImageTk
from io import BytesIO
from time import time
from modules.open_webpage import ask_open

from modules.data import save_settings, icon_path, version, settings
from modules.tempdata import opened_windows, params

from modules.windows.debug import run as open_debug
from modules.windows.settings import run as open_settings

class MainWindow:
    def __init__(self, root: ThemedTk):
        self.root = root
        self.root.configure(bg="#464646")
        root.iconbitmap(icon_path)
        self.icon = None
        root.iconbitmap(icon_path)
        root.minsize(280, 90)
        root.title(f"RPC {version}")
        self.disable_maximize_button()
        self.connected = tk.BooleanVar(value=settings.get('on', False))
        app_checkbox = Checkbutton(root, text="Подключиться", variable=self.connected, command=self.update_status)

        self.name = tk.StringVar()
        self.author = tk.StringVar()
        
        name_label = Label(root, textvariable=self.name)
        author_label = Label(root, textvariable=self.author)
        self.image_label = Label(root)

        self.update_status()
        self.editImage('https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Icon.png')

        button_frame = tk.Frame(root, bg="#464646")
        settings_button = Button(button_frame, text='Настройки', command=open_settings)
        error_button = Button(button_frame, text='Сообщить об ошибке', command=self.open_github_issues)
        debug_button = Button(button_frame, text='Отладка', command=open_debug)

        settings_button.grid(row=0, column=0, sticky="w")
        error_button.grid(row=0, column=1, sticky="w")
        debug_button.grid(row=0, column=2, sticky="w")

        button_frame.grid(row=0, column=0, columnspan=100, sticky="wn")

        self.image_label.grid(row=1, column=0, rowspan=9, columnspan=4, sticky="e", padx=5, pady=5)
        app_checkbox.grid(row=2, column=5, columnspan=96, sticky="w", padx=5)
        name_label.grid(row=5, column=5, columnspan=96, sticky="w", padx=5)
        author_label.grid(row=7, column=5, columnspan=96, sticky="w", padx=5)

        root.protocol("WM_DELETE_WINDOW", self.withdraw_window)
        root.bind("<Button-1>", self.on_drag_start)
        root.bind("<B1-Motion>", self.on_drag_motion)

    def disable_maximize_button(self):
        hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())

        ctypes.windll.user32.SetWindowLongW(hwnd, ctypes.c_int(-16), ctypes.c_long(
            ctypes.windll.user32.GetWindowLongW(hwnd, ctypes.c_int(-16)) & ~0x00010000))
        
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

    def show_window(self, icon, item):
        icon.stop()
        self.icon = None
        opened_windows.main_hiden = False
        self.root.after(0, self.root.deiconify)

    def open_github_issues(self):
        ask_open("https://github.com/Soto4ka37/Yandex-Music-RPC-Lite/issues")

    def open_github(self, icon, item):
        icon.stop()
        self.icon = None
        opened_windows.main_hiden = False
        self.root.after(0, self.root.deiconify)
        ask_open("https://github.com/Soto4ka37/Yandex-Music-RPC-Lite/")

    def withdraw_window(self):  
        opened_windows.close_sub_windows()

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
            opened_windows.close_all()

def run():
    main_window = ThemedTk(theme='equilux')
    main_window = MainWindow(main_window)
    opened_windows.main = main_window
    main_window.root.mainloop()