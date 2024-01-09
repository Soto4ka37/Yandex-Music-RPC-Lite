import os

def run():
    print('Установка необходимых модулей...')
    with open('requirements.txt', 'r') as file:
        requirements = file.read()
        pip = requirements.replace('\n', ' ')
        os.system(f"pip install -U {pip}")

if __name__ == "__main__":
    run()