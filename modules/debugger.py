from datetime import datetime

_debug = []
_last_time = None

def lastTime() -> str:
    global _last_time

    current_time = datetime.now()
    if _last_time is None:
        _last_time = current_time
        return "🙂"

    time_difference = current_time - _last_time
    _last_time = current_time

    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = time_difference.microseconds // 1000
    result = []
    if hours > 0:
        result.append(f"{hours}ч")
    if minutes > 0:
        result.append(f"{minutes}м")
    if seconds > 0 and not hours:
        result.append(f"{seconds}с")
    if milliseconds and not minutes:
        result.append(f"{milliseconds}мс")
    if not result:
        result.append('0мс')

    return ", ".join(result)

def addInfo(text: str):
    text = f'[I] [{lastTime()}] {text}'
    _debug.append(text)

def addRequest(text: str):
    text = f'[R] [{lastTime()}] {text}'
    _debug.append(text)

def addWarning(text: str):
    text = f'[W] [{lastTime()}] {text}'
    _debug.append(text)

def addError(text: str):
    text = f'[E] [{lastTime()}] {text}'
    _debug.append(text)

def getList() -> list:
    '''Возвращает отладку ввиде списка'''
    return _debug

def getString() -> str:
    '''Возвращает отладку ввиде строки'''
    return '\n'.join(_debug) + '\n'

addInfo('Отладка запущена.')
