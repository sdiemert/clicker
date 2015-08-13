import wx
from AppFrame import AppFrame
from Controller import Controller

control = Controller()

app = wx.App(False)  # don't redirect stdout/stderr, create new app.

frame = AppFrame(None, "Clicker Uploader", control)


app.MainLoop()
