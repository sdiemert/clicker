__author__ = 'sdiemert'

import wx

class AppFrame(wx.Frame):

    def __init__(self, parent, title, controller=None):
        wx.Frame.__init__(self, parent, title=title, size=(800, 600))

        self.controller = controller

        self.SetMaxSize(wx.Size(800, 600))

        self.display = wx.Panel(self, wx.ID_ANY)

        self.title = wx.StaticText(self.display, wx.ID_ANY, "Clicker Client")
        self.divider = wx.StaticLine(self.display, wx.ID_ANY)
        self.arduino_upload_button = wx.Button(self.display, wx.ID_ANY, "Load from Arduino")
        self.http_upload_button = wx.Button(self.display, wx.ID_ANY, "Upload to Web")
        self.cancel_button = wx.Button(self.display, wx.ID_ANY, "Cancel")
        self.input1 = wx.ComboBox(self.display, wx.ID_ANY, value="Select Source", choices=['a', 'b', 'c'],
                                  size=(400, -1))
        self.output = wx.TextCtrl(self.display, wx.ID_ANY, size=(800, 400), style=wx.TE_MULTILINE)

        self.title.SetFont(wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL))
        self.output.SetEditable(False)
        self.http_upload_button.Disable()

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
        control.Add(self.arduino_upload_button, 0, wx.ALL, 5)
        control.Add(self.http_upload_button, 0, wx.ALL, 5)
        control.Add(self.cancel_button, 0, wx.ALL, 5)

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
        self.Bind(wx.EVT_BUTTON, self._on_upload_action, self.arduino_upload_button)
        self.Bind(wx.EVT_BUTTON, self._on_http_action, self.http_upload_button)
        self.Bind(wx.EVT_BUTTON, self._on_cancel_action, self.cancel_button)

        self.CreateStatusBar()

        filemenu = wx.Menu()
        filemenu.Append(wx.ID_ABOUT, '&About', "Information about this program")
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, 'E&xit', "Exit this program")
        menubar = wx.MenuBar()
        menubar.Append(filemenu, "&File")

        self.SetMenuBar(menubar)

        self.Show(True)

    def set_controller(self, controller):
        self.controller = controller

    def _on_http_action(self, event):
        print "HTTP Action"
        pass

    def _on_cancel_action(self, events):
        print "Cancel Action"
        self.output.Clear()
        self.http_upload_button.Disable()
        self.arduino_upload_button.Enable()
        self.controller.reset()

    def _on_upload_action(self, event):
        """
        Handles the case where the upload button is pressed.

        :param event: the event object that contains information about the action.
        :return: None
        """
        print "Upload Action"

        if not self.controller:
            raise RuntimeError("Controller not set, Upload button click not handled.")
        else:
            self.output.Clear()
            if self.controller.upload(self.input1.GetValue()):
                self.http_upload_button.Enable()
                self.arduino_upload_button.Disable()
                self.display_message("-------------------------")
                self.controller.show_data()
                self.display_message("-------------------------")
                self.display_message("Select 'Upload to Web' to send this data to the web app...")

    def display_message(self, message, level=1):
        """
        :param s:
        :param level: 0,1,2: DEBUG, INFO, ERROR
        :return:
        """
        s = ""
        if level == 1:
            s += "[INFO] "
        elif level == 0:
            s += "[DEBUG] "
        elif level == 2:
            s += "[ERROR] "

        s += message

        self.output.AppendText(s+"\n")

    def populate(self):

        if self.controller:
            d = self.controller.get_interfaces()
            self.input1.Clear()
            self.input1.AppendItems(d)
            self.input1.SetValue(d[0])

        return None
