__author__ = 'sdiemert'

import wx


class AppFrame(wx.Frame):
    def __init__(self, parent, title, controller):
        wx.Frame.__init__(self, parent, title=title, size=(800, 600))

        self.SetMaxSize(wx.Size(800, 600))

        self.display = wx.Panel(self, wx.ID_ANY)

        self.title = wx.StaticText(self.display, wx.ID_ANY, "Clicker Client")
        self.divider = wx.StaticLine(self.display, wx.ID_ANY)
        self.upload_button = wx.Button(self.display, wx.ID_ANY, "Go!")
        self.input1 = wx.ComboBox(self.display, wx.ID_ANY, value="Select Source", choices=['a', 'b', 'c'],
                                  size=(200, -1))
        self.output = wx.TextCtrl(self.display, wx.ID_ANY, size=(800, 400), style=wx.TE_MULTILINE)

        self.title.SetFont(wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL))
        self.output.SetEditable(False)

        wrapper = wx.BoxSizer(wx.VERTICAL)
        top = wx.BoxSizer(wx.HORIZONTAL)
        content = wx.BoxSizer(wx.VERTICAL)
        control = wx.BoxSizer(wx.HORIZONTAL)
        feedback = wx.BoxSizer(wx.HORIZONTAL)
        bottom = wx.BoxSizer(wx.HORIZONTAL)

        top.Add(self.title, 0, wx.ALL, 5)

        # controls the height of the top bar.
        top.SetMinSize(wx.Size(-1, -1))

        control.Add(self.input1, 0, wx.ALL, 5)
        control.Add(self.upload_button, 0, wx.ALL, 5)

        feedback.Add(self.output, 0, wx.ALL, 5)

        content.Add(control, 0, wx.ALL, 5)
        content.Add(feedback, 0, wx.ALL, 5)

        wrapper.Add(top, 0, wx.ALL, 5)
        wrapper.Add(self.divider, 0, wx.ALL | wx.EXPAND, 5)
        wrapper.Add(content, 0, wx.ALL, 5)
        wrapper.Add(bottom, 0, wx.ALL | wx.EXPAND, 5)

        self.display.SetSizer(wrapper)

        wrapper.Fit(self)

        # Bind action handlers to UI elements:
        self.Bind(wx.EVT_BUTTON, self.on_upload_action, self.upload_button)

        self.CreateStatusBar()

        filemenu = wx.Menu()
        filemenu.Append(wx.ID_ABOUT, '&About', "Information about this program")
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, 'E&xit', "Exit this program")
        menubar = wx.MenuBar()
        menubar.Append(filemenu, "&File")

        self.SetMenuBar(menubar)

        self.Show(True)

    def on_upload_action(self, event):
        """
        Handles the case where the upload button is pressed.

        :param event: the event object that contains information about the action.
        :return: None
        """
        print "Upload button clicked!"

