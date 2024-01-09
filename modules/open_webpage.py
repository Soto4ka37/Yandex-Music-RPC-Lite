import webbrowser
from tkinter import messagebox
def ask_open(url: str):
    a = messagebox.askquestion('Сторонняя ссылка', f'Вы действительно хотите открыть ссылку {url} в своём брауезере?')
    if a == 'yes':
        webbrowser.open(url)
