
import tkinter as tk
from tkinter.ttk import Scrollbar
import modules.debugger as debugger
from modules.tempdata import opened_windows

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

def run():
    if opened_windows.debugger:
        return
    
    debug_window = tk.Toplevel()
    debug_window = DebugWindow(debug_window)
    opened_windows.debugger = debug_window