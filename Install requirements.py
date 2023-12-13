import os

def __AutoRun():
    print('Установка необходимых модулей...')
    os.system(f"pip install pystray requests yandex_music pillow pypresence selenium==4.8.1 wxPython")
    input('\n\nУстановка модулей успешно завершена! Нажмите Enter, что бы закрыть окно.')

def run():
    print('Установка необходимых модулей...')
    os.system(f"pip install pystray requests yandex_music pillow pypresence selenium==4.8.1 wxPython")
    print('Установка модулей успешно завершена!')
if __name__ == "__main__":
    __AutoRun()