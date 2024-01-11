import tkinter as tk
import keyboard

def on_copy(event):
    event.widget.event_generate('<<Copy>>')

def on_cut(event):
    event.widget.event_generate('<<Cut>>')

def on_paste(event):
    event.widget.event_generate('<<Paste>>')

root = tk.Tk()
text_widget = tk.Text(root)
text_widget.pack()

# Привязываем события копирования, вырезания и вставки к функциям
text_widget.bind('<Control-c>', on_copy)
text_widget.bind('<Control-x>', on_cut)
text_widget.bind('<Control-v>', on_paste)

# Проверяем текущую раскладку клавиатуры с использованием библиотеки keyboard
def check_keyboard_layout(event):
    current_layout = keyboard.get_keyboard_layout()
    if current_layout == 'Russian':
        # Раскладка русская, обрабатываем события клавиш
        text_widget.bind('<Control-а>', on_copy)
        text_widget.bind('<Control-я>', on_cut)
        text_widget.bind('<Control-ь>', on_paste)
    else:
        # Раскладка не русская, снимаем привязку событий
        text_widget.unbind('<Control-а>')
        text_widget.unbind('<Control-я>')
        text_widget.unbind('<Control-ь>')

# Привязываем функцию проверки раскладки к событию нажатия клавиши
root.bind('<KeyPress>', check_keyboard_layout)

root.mainloop()