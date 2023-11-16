from time import strftime
debug = []
def now() -> str:
    '''Возвращает текующую дату и время'''
    return strftime('%Y-%m-%d %H:%M')

class Debug():
    def add(text: str):
        '''Добавить объект в откладку'''
        text = f'[{now()}] {text}'
        debug.append(text)

    def get() -> list:
        '''Возвращает откладку ввиде списка'''
        return debug
    def get_str() -> str:
        '''Возвращает откладку ввиде строки'''
        return '\n\n'.join(debug)
