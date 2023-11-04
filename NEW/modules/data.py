import json
default = {
  "ping": 1,
  "t_time": 2,
  "t_button": True,
  "w_time": True,
  "n_clear": False,
  "n_time": True,
  "on": False,
  "token": "0"
}
def load_settings():
    try:
        with open('data.json', 'r') as file:
            settings = json.load(file)
        return settings
    except FileNotFoundError:
        return default

def save_settings(settings):
    with open('data.json', 'w') as file:
        json.dump(settings, file, indent=4)
