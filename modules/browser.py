from wx import ListBox, App, Frame, BoxSizer, VERTICAL, EXPAND, Button, EVT_BUTTON
from wx.html2 import WebView, EVT_WEBVIEW_NEWWINDOW, EVT_WEBVIEW_NAVIGATED
import wx.adv
import sys

class WebBrowser(Frame):
    address = []
    browser = []
    history = []

    def OnLoad(self, event):
        self.webtitle = self.browser.GetCurrentURL()
        return

    def NewWindow(self, event):
        self.browser.LoadURL(event.URL)

    def __init__(self, parent, title):

        Frame.__init__(self, parent, id=-1, title=title)
        sizer = BoxSizer(VERTICAL)

        self.browser = WebView.New(self)


        sizer.Add(self.browser, proportion=80, flag=EXPAND, border=10)

        self.SetSizer(sizer)
        self.SetSize((700, 900))

        self.Bind(EVT_WEBVIEW_NAVIGATED, self.OnLoad, self.browser)
        self.Bind(EVT_WEBVIEW_NEWWINDOW, self.NewWindow, self.browser)
    
        self.tbicon = wx.adv.TaskBarIcon()
        self.tbicon.SetIcon(wx.Icon("assets/icon.ico"), "Яндекс Музыка")
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        self.tbicon.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.OnLeftClick)
        self.tbicon.Bind(wx.adv.EVT_TASKBAR_RIGHT_DOWN, self.OnRightClick)

    def OnClose(self, event):
        self.Hide()
        message = "Приложение свёрнуто в системный трей"
        caption = "Яндекс Музыка - Фоновый Режим"
        
        dialog = wx.MessageDialog(self, message, caption, wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION)
        dialog.SetYesNoLabels("Выход", "Ок")
        
        result = dialog.ShowModal()
        if result == wx.ID_YES:
            sys.exit(0)
        
        dialog.Destroy()
        event.Veto()
        
    def OnLeftClick(self, event):
        self.Show()
        self.Iconize(False)
    def OnRightClick(self, event):
        menu = wx.Menu()
        
        open_item = menu.Append(wx.ID_ANY, "Открыть")
        self.Bind(wx.EVT_MENU, self.OnOpen, open_item)
        
        yandex_music_item = menu.Insert(1, wx.ID_ANY, "Открыть music.yandex.ru")
        self.Bind(wx.EVT_MENU, self.OnYandexMusicClicked, yandex_music_item)

        github_item = menu.Insert(1, wx.ID_ANY, "Открыть GitHub")
        self.Bind(wx.EVT_MENU, self.OnGitHubClicked, github_item)
        
        exit_item = menu.Append(wx.ID_ANY, "Выход")
        self.Bind(wx.EVT_MENU, self.OnExit, exit_item)
        
        self.PopupMenu(menu)
        menu.Destroy()

    def OnOpen(self, event):
        self.Show()
        self.Iconize(False)

    def OnGitHubClicked(self, event):
        self.browser.LoadURL("https://github.com/Soto4ka37/Yandex-Music-RPC-Lite/")
        self.Show()
        self.Iconize(False)

    def OnYandexMusicClicked(self, event):
        self.browser.LoadURL("https://music.yandex.ru/")
        self.Show()
        self.Iconize(False)

    def OnRefreshButtonClicked(self, event):
        self.browser.Reload()

    def OnExit(self, event):
        sys.exit(0)
        
app = App()
main_window = WebBrowser(None, "Яндекс Музыка")
main_window.browser.LoadURL("https://music.yandex.ru/")
main_window.Show()
app.MainLoop()