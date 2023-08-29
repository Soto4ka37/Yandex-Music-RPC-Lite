from configparser import ConfigParser

import wx
from wx import App, Frame, EVT_CLOSE
from wx.html2 import WebView

config = ConfigParser()
config.read('settings.ini')


class TokenFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent, title="Логин", size=(450, 600))

        self.browser = WebView.New(self)
        self.browser.Bind(wx.html2.EVT_WEBVIEW_NAVIGATING, self.OnUrlChanged)

        self.Bind(EVT_CLOSE, self.OnClose)

    def OnUrlChanged(self, event):
        url = event.GetURL()
        print(url)
        if "#access_token" in url:
            print(url.split("=")[1].split("&")[0])
            self.token = url.split("=")[1].split("&")[0]
            self.Destroy()

    def OnClose(self, event):
        self.token = None
        self.Destroy()


def UpdateToken():
    app = App(redirect=False)
    token_frame = TokenFrame(None)
    token_frame.browser.LoadURL(
        "https://oauth.yandex.ru/authorize?response_type=token&client_id=23cabbbdc6cd418abb4b39c32c41195d")
    token_frame.Show()
    app.MainLoop()
    print(token_frame.token)
    return token_frame.token
