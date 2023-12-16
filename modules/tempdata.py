from modules.presense import RPC
class OpenedWidnows:
    def __init__(self):
        self.main = None
        self.settings = None
        self.status_editor = None
        self.buttons_editor = None
        self.debugger = None
        self.main_hiden = False

class Params:
    def __init__(self):
        self.lastclick = 0
        self.exit = False
        self.lasttrack = None
        self.lastradio = None
        self.nowplaymode = None
        self.rpc = None
        self.need_notify = False
        self.need_update_main_window = False


    def reloadStatus(self):
        self.nowplaymode = None
        self.lasttrack = None
        self.lastradio = None

    def createRPC(self):
        self.closeRPC()
        rpc = RPC()
        self.rpc = rpc
        return rpc
    
    def closeRPC(self):
        if self.rpc:
            try:
                self.rpc.disconnect()
            except:
                pass
        self.rpc = None

opened_windows = OpenedWidnows()
params = Params()