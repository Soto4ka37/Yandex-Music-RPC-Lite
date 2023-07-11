from wx import ListBox, App, Frame, BoxSizer, VERTICAL, LB_SINGLE, EXPAND
from wx.html2 import WebView, EVT_WEBVIEW_NEWWINDOW, EVT_WEBVIEW_NAVIGATED
import wx.adv
import sys

class WebBrowser(Frame):
    address = []
    browser = []
    history = []

    def OnLoad(self, event):
        self.webtitle = self.browser.GetCurrentURL()
        self.history.InsertItems([self.webtitle], 0)
        return

    def NewWindow(self, event):
        title = self.browser.GetCurrentTitle()
        self.SetTitle(title)
        second_window = WebBrowser(None, title=title)
        second_window.browser.LoadURL(event.URL)
        second_window.Show()

    def __init__(self, parent, title):

        Frame.__init__(self, parent, id=-1, title=title)
        sizer = BoxSizer(VERTICAL)

        self.browser = WebView.New(self)
        self.history = ListBox(self, size=(100, -1), style=LB_SINGLE)

        sizer.Add(self.browser, proportion=80, flag=EXPAND, border=10)

        self.SetSizer(sizer)
        self.SetSize((600, 800))

        self.Bind(EVT_WEBVIEW_NAVIGATED, self.OnLoad, self.browser)
        self.Bind(EVT_WEBVIEW_NEWWINDOW, self.NewWindow, self.browser)
    
        self.tbicon = wx.adv.TaskBarIcon()
        self.tbicon.SetIcon(wx.Icon("assets/icon.ico"), "Яндекс Музыка")
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        self.tbicon.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.OnLeftClick)
        
        self.tbicon.Bind(wx.adv.EVT_TASKBAR_RIGHT_DOWN, self.OnRightClick)

    def OnClose(self, event):
        self.Hide()
        wx.MessageBox("Приложение продолжит работать в фоновом режиме.\nЧтобы его открыть нажмите на иконку в трее.", "Яндекс музыка", wx.OK | wx.ICON_INFORMATION)
        event.Veto()
        
    def OnLeftClick(self, event):
        self.Show()
        
    def OnRightClick(self, event):
        menu = wx.Menu()
        
        open_item = menu.Append(wx.ID_ANY, "Открыть")
        self.Bind(wx.EVT_MENU, self.OnOpen, open_item)
        
        exit_item = menu.Append(wx.ID_ANY, "Выход")
        self.Bind(wx.EVT_MENU, self.OnExit, exit_item)
        
        self.PopupMenu(menu)
        menu.Destroy()

    def OnOpen(self, event):
        self.Show()

    def OnExit(self, event):
        sys.exit(0)
        
app = App()
main_window = WebBrowser(None, "Яндекс Музыка")
main_window.browser.LoadURL("https://music.yandex.ru/")
main_window.Show()
app.MainLoop()