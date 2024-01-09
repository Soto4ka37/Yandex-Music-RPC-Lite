from modules.data import save_settings, settings, get_icon, icon_path, version
from modules.update import check_updates
import modules.debugger as debugger

if settings.get('update'):
    debugger.addInfo(f'Текущая версия программы: {version}')
    check_updates(version)

from modules.tempdata import opened_windows, params

from time import sleep, time
import traceback
import os
import sys
from threading import Thread
from pypresence import exceptions
from tkinter import messagebox

from modules.api import getClient, API, NotQueue
from modules.windows.main_window import run as open_gui

if not os.path.exists(icon_path):
    get_icon()

def yandex_music_rpc():
    main_find = opened_windows.wait_main()
    if not main_find:
        return
    song = API(params.client)
    while not params.exit and opened_windows.main:
        if opened_windows.main.icon and params.need_notify:
            opened_windows.main.icon.notify(title='Yandex Music RPC', message='Приложение работет в фоновом режиме')
            params.need_notify = False
        try:
            if params.rpc:
                if settings.get("on"):
                    song.update()
                    if song.fulldone:
                        if song.link != params.lasttrack:
                            params.reloadStatus()
                            params.lasttrack = song.url

                            if settings.get('on'):
                                params.rpc.update(song)

                                if not opened_windows.main_hiden:
                                    details = params.rpc.param_to_text(settings.get('tr_details'), song)
                                    state = params.rpc.param_to_text(settings.get('tr_state'), song)
                                    opened_windows.main.editName(details)
                                    opened_windows.main.editAuthor(state)
                                    if settings.get('image'):
                                        opened_windows.main.editImage(song.icon)
                                else:
                                    params.need_update_main_window = True

                            else:
                                continue
                            
                            lastupdate = time()
                            params.nowplaymode = 1

                        elif settings.get('t_time') and params.nowplaymode != 2:
                            if time() - lastupdate >= song.total: # Если прошло больше веремени чем длинна трека переходим в режим повтора
                                params.reloadStatus()
                                params.lasttrack = song.url
                                
                                if settings.get('on'):
                                    params.rpc.repeat(song, lastupdate)
                                    if not opened_windows.main_hiden:
                                        details = params.rpc.param_to_text(settings.get('re_details'), song)
                                        state = params.rpc.param_to_text(settings.get('re_state'), song)
                                        opened_windows.main.editName(details)
                                        opened_windows.main.editAuthor(state)
                                    else:
                                        params.need_update_main_window = True

                                else:
                                    continue

                                if settings.get('t_time', 2) == 1:
                                    lastupdate = time()

                                elif settings.get('t_time', 2) == 2:
                                    params.nowplaymode = 2

                    elif song.partdone and song.type and song.type == 'radio':
                            if song.description != params.lastradio:
                                params.reloadStatus()
                                params.lastradio = song.description

                                if settings.get('on'):
                                    params.rpc.wave(song=song)
                                    if not opened_windows.main_hiden:
                                        details = params.rpc.param_to_text(settings.get('ww_details'), song)
                                        state = params.rpc.param_to_text(settings.get('ww_state'), song)
                                        opened_windows.main.editName(details)
                                        opened_windows.main.editAuthor(state)
                                        if settings.get('image'):
                                            opened_windows.main.editImage('https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Wave.png')
                                    else:
                                        params.need_update_main_window = True

                                else:
                                    continue

                                params.nowplaymode = 3
                    else:
                        if params.nowplaymode != 0:
                            params.reloadStatus()
                            debugger.addWarning('Не удалось определить текущий трек. Возвращён пустой ответ.')
                            params.rpc.nodata(song)
                            params.nowplaymode = 0
                            if settings.get('on'):
                                if not opened_windows.main_hiden:
                                    details = settings.get('no_details')
                                    state = settings.get('no_state')
                                    opened_windows.main.editName(details)
                                    opened_windows.main.editAuthor(state)
                                    if settings.get('image'):
                                        opened_windows.main.editImage('https://music.yandex.ru/blocks/playlist-cover/playlist-cover_no_cover4.png')
                                else:
                                    params.need_update_main_window = True
                                    
                            else:
                                continue
                    
                    if params.need_update_main_window and not opened_windows.main_hiden:
                        if params.nowplaymode == 0:
                            details = settings.get('no_details')
                            state = settings.get('no_state')
                            image = 'https://music.yandex.ru/blocks/playlist-cover/playlist-cover_no_cover4.png'
                        elif params.nowplaymode == 1:
                            details = params.rpc.param_to_text(settings.get('tr_details'), song)
                            state = params.rpc.param_to_text(settings.get('tr_state'), song)
                            image = song.icon
                        elif params.nowplaymode == 2:
                            details = params.rpc.param_to_text(settings.get('re_details'), song)
                            state = params.rpc.param_to_text(settings.get('re_state'), song)
                            image = song.icon
                        else:
                            details = params.rpc.param_to_text(settings.get('ww_details'), song)
                            state = params.rpc.param_to_text(settings.get('ww_state'), song)
                            image = 'https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Wave.png'

                        opened_windows.main.editName(details)
                        opened_windows.main.editAuthor(state)
                        params.need_update_main_window = False
                        if settings.get('image'):
                            opened_windows.main.editImage(image)

                    sleep(settings.get('ping'))

                else:
                    params.rpc.clear()
                    params.reloadStatus()
                    debugger.addError('Отсутсвует ответ от API')
                    sleep(3)

            else:
                sleep(settings.get('ping'))

        except Exception as e:
            #print(traceback.format_exc())
            if isinstance(e, (exceptions.PipeClosed, exceptions.InvalidPipe, RuntimeError)):
                params.closeRPC()
                params.reloadStatus()
                opened_windows.main.editConnect(False)
                settings['on'] = False
                save_settings(settings)

                opened_windows.main.editName('Соединение с Discord разорвано')
                opened_windows.main.editAuthor()
                if settings.get("image"):
                    opened_windows.main.editImage('https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Icon.png')

                debugger.addWarning(f'Соединение с дискордом разорвано')

            elif isinstance(e, NotQueue):
                params.closeRPC()
                params.reloadStatus()

                opened_windows.main.editConnect(False)
                settings['on'] = False
                save_settings(settings)

                opened_windows.main.editName('Возвращена пустая очерерь')
                opened_windows.main.editAuthor('API не вернул никаких результатов для текущего аккаунта')
                if settings.get("image"):
                    opened_windows.main.editImage('https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Icon.png')

                debugger.addError(f'API не вернул никаких результатов для текущего аккаунта')

            else:
                error = traceback.format_exc()
                params.closeRPC()
                params.reloadStatus()

                opened_windows.main.editConnect(False)
                settings['on'] = False
                save_settings(settings)

                opened_windows.main.editName('Критическая ошибка')
                opened_windows.main.editAuthor()
                if settings.get("image"):
                    opened_windows.main.editImage('https://raw.githubusercontent.com/Soto4ka37/Yandex-Music-RPC-Lite/master/assets/RPC-Icon.png')

                debugger.addError(f'Непредвиденное исключение\n{error}')
                messagebox.showerror('Yandex Music RPC | Непредвиденное исключение', message=f'{error}')

if __name__ == "__main__":    
    t1 = Thread(target=open_gui)
    t1.start()
    
    t2 = Thread(target=yandex_music_rpc)
    t2.start()

    t2.join()