import wx

class MyFrame(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(200, 100))

        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        self.display = wx.Panel(self, wx.ID_ANY)
        self.static = wx.StaticText(self.display, wx.ID_ANY, "static text")
        self.CreateStatusBar()

        filemenu = wx.Menu()
        aboutItem = filemenu.Append(wx.ID_ABOUT, '&About', "Information about this program")

        filemenu.AppendSeparator()

        exitItem = filemenu.Append(wx.ID_EXIT, 'E&xit', "Exit this program")

        other = filemenu.Append(1010, 'foobar', "does a foobar")
        self.Bind(wx.EVT_MENU, self.OnFooBar, other)
        
        menubar = wx.MenuBar()
        menubar.Append(filemenu, "&File")

        self.SetMenuBar(menubar)

        self.Show(True)

    def OnFooBar(self, event):
        print "foobar!"


app = wx.App(False) #don't redirect stdout/stderr, create new app.
frame = MyFrame(None, "Small Editor") 
app.MainLoop()
