import tkinter as tk
from tkinter import ttk
from modules.data import version

class CustomTitleBar(tk.Frame):
    def __init__(self, master=None, title: str = f'RPC {version}', is_settings: bool = False):
        super().__init__(master, height=30, bg="#464646")
        self.title_label = ttk.Label(self, text=title)
        self.title_label.pack(side=tk.LEFT, padx=5)
        self.master.attributes('-topmost', 1)
        if not is_settings:
            self.settings_button = ttk.Button(self, text="Настройки", command=self.minimize)
            self.settings_button.pack(side=tk.LEFT)
        self.close_button = ttk.Button(self, text="X", command=self.close)
        self.close_button.pack(side=tk.RIGHT)

        if not is_settings:
            self.minimize_button = ttk.Button(self, text="—", command=self.minimize)
            self.minimize_button.pack(side=tk.RIGHT)
        if is_settings:
            self.bind("<B1-Motion>", self.drag)
            self.bind("<Button-1>", self.start_drag)
            self.bind("<ButtonRelease-1>", self.stop_drag)

            self.drag_data = {"x": 0, "y": 0}

    def minimize(self):
        pass
        

    def close(self):
        self.master.destroy()

    def start_drag(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def stop_drag(self, event):
        self.drag_data = {"x": 0, "y": 0}

    def drag(self, event):
        x = self.winfo_pointerx() - self.drag_data["x"]
        y = self.winfo_pointery() - self.drag_data["y"]
        self.master.geometry(f"+{x}+{y}")