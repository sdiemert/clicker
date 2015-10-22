__author__ = 'sdiemert'

import wx

from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin


class AutoWidthListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent, size=(200, 400)):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT, size=size)
        ListCtrlAutoWidthMixin.__init__(self)


class AppFrame(wx.Frame):
    def __init__(self, parent, title, controller=None):
        wx.Frame.__init__(self, parent, title=title, size=(1000, 800))

        self.listCount = 0

        self.controller = controller

        self.SetMaxSize(wx.Size(800, 800))

        self.display = wx.Panel(self, wx.ID_ANY)

        self.title = wx.StaticText(self.display, wx.ID_ANY, "SPARC Change Connector")
        self.divider = wx.StaticLine(self.display, wx.ID_ANY)
        self.arduino_upload_button = wx.Button(self.display, wx.ID_ANY, "Load from Arduino")
        self.http_upload_button = wx.Button(self.display, wx.ID_ANY, "Upload to Web")
        self.cancel_button = wx.Button(self.display, wx.ID_ANY, "Cancel")
        self.input1 = wx.ComboBox(self.display, wx.ID_ANY, value="Select Source", choices=['a', 'b', 'c'],
                                  size=(400, -1))
        self.initiatives = wx.ComboBox(self.display, wx.ID_ANY, value="Select Initiative", choices=['a', 'b', 'c'],
                                       size=(300, -1))
        self.init_label = wx.StaticText(self.display, wx.ID_ANY, "Initiative:")
        self.members = wx.ComboBox(self.display, wx.ID_ANY, value="Select Member", choices=['a', 'b', 'c'],
                                   size=(300, -1))
        self.member_label = wx.StaticText(self.display, wx.ID_ANY, "Actua Member:")

        self.output = wx.TextCtrl(self.display, wx.ID_ANY, size=(500, 600), style=wx.TE_MULTILINE)
        self.user_label =  wx.StaticText(self.display, wx.ID_ANY, "Username (leave blank if none):")
        self.user = wx.TextCtrl(self.display, wx.ID_ANY, size=(100, 25))
        # self.remove_button = wx.Button(self.display, wx.ID_ANY, "Remove Items")

        self.title.SetFont(wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL))
        self.output.SetEditable(False)
        self.http_upload_button.Disable()
        # self.remove_button.Disable()

        self.initiatives.Disable()
        self.members.Disable()

        self.list = AutoWidthListCtrl(self.display, size=(400, 300))
        self.generate_list_cols()

        wrapper = wx.BoxSizer(wx.VERTICAL)
        top = wx.BoxSizer(wx.HORIZONTAL)
        content = wx.BoxSizer(wx.VERTICAL)
        control = wx.BoxSizer(wx.HORIZONTAL)
        feedback = wx.BoxSizer(wx.HORIZONTAL)
        data = wx.BoxSizer(wx.VERTICAL)
        data_control = wx.BoxSizer(wx.VERTICAL)
        data_buttons = wx.BoxSizer(wx.HORIZONTAL)
        bottom = wx.BoxSizer(wx.HORIZONTAL)

        top.Add(self.title, 0, wx.ALL, 5)

        # controls the height of the top bar.
        top.SetMinSize(wx.Size(-1, -1))

        control.Add(self.input1, 0, wx.ALL, 5)
        control.Add(self.arduino_upload_button, 0, wx.ALL, 5)
        control.Add(self.cancel_button, 0, wx.ALL, 5)

        data.Add(self.list, 0, wx.ALL, 5)

        # data_buttons.Add(self.remove_button, 0, wx.ALL, 5)
        data_buttons.Add(self.http_upload_button, 0, wx.ALL, 5)

        data_control.Add(data_buttons)

        data.Add(self.init_label, 0, wx.ALL, 5)
        data.Add(self.initiatives, 0, wx.ALL, 5)
        data.Add(self.member_label, 0, wx.ALL, 5)
        data.Add(self.members, 0, wx.ALL, 5)
        data.Add(self.user_label, 0, wx.ALL, 5)
        data.Add(self.user, 0, wx.ALL, 5)
        data.Add(data_control)

        feedback.Add(self.output, 0, wx.ALL, 5)

        feedback.Add(data, 0, wx.ALL, 5)

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
        # self.Bind(wx.EVT_BUTTON, self._on_remove_button, self.remove_button)

        self.Bind(wx.EVT_COMBOBOX, self._on_init_select, self.initiatives)

        self.CreateStatusBar()

        filemenu = wx.Menu()
        filemenu.Append(wx.ID_ABOUT, '&About', "Information about this program")
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, 'E&xit', "Exit this program")
        menubar = wx.MenuBar()
        menubar.Append(filemenu, "&File")

        self.SetMenuBar(menubar)

        self.Show(True)

    def generate_list_cols(self):
        self.list.InsertColumn(0, 'Item No.', width=60)
        self.list.InsertColumn(1, 'Button', width=60)
        self.list.InsertColumn(2, 'Action', width=140)
        self.list.InsertColumn(3, 'Date', width=80)

    def _on_init_select(self, event):
        print "Initiative Select: " + self.initiatives.GetValue()

        self.apply_initiative(self.initiatives.GetValue())

    def _on_remove_button(self, event):
        print "Remove Button"

    def set_controller(self, controller):
        self.controller = controller

    def _on_http_action(self, event):
        print "HTTP Action"
        username = self.user.GetValue()

        if username == "":
            username = None

        self.controller.send_data(username)
        pass

    def add_list_item(self, val):

        if len(val) != 2:
            raise TypeError("AppFrame.add_list_item(val) expects val to be a tuple of length 2")

        index = self.list.InsertStringItem(self.listCount, str(self.listCount))

        if index >= 0:

            print val

            self.list.SetStringItem(index, 1, val[0])
            self.list.SetStringItem(index, 3, val[1])
            self.listCount += 1
            return True

        else:
            return False

    def _on_cancel_action(self, events):
        print "Cancel Action"
        self.reset()

    def reset(self):
        self.output.Clear()
        self.http_upload_button.Disable()
        self.arduino_upload_button.Enable()
        self.initiatives.Disable()
        self.members.Disable()
        self.controller.reset()
        self.reset_list()

    def reset_list(self):
        self.list.ClearAll()
        self.listCount = 0

        # Calling list.ClearAll() removes columns
        # so  we must re-generate them.
        self.generate_list_cols()

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
            self.reset()
            if self.controller.upload(self.input1.GetValue()):
                self.http_upload_button.Enable()
                self.arduino_upload_button.Disable()
                self.initiatives.Enable()
                self.members.Enable()
                self.display_message("-------------------------")
                self.controller.show_data()
                self.display_message("-------------------------")
                self.display_message("Select 'Upload to Web' to send this data to the web.")
                data = self.controller.get_data()

                if data:
                    for d in data:
                        self.add_list_item(d.get_list_rep())
                    self.apply_initiative(self.initiatives.GetValue())
            else:
                self.reset()

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

        self.output.AppendText(s + "\n")

    def populate(self):

        if self.controller:
            d = self.controller.get_interfaces()
            self.input1.Clear()
            self.input1.AppendItems(d)
            self.input1.SetValue(d[0])

            i = self.controller.get_initiatives()
            self.initiatives.Clear()
            self.initiatives.AppendItems(i)
            self.initiatives.SetValue(i[0])

            m = self.controller.get_members()
            self.members.Clear()
            self.members.AppendItems(m)
            self.members.SetValue(m[0])

        return None

    def apply_tags_to_list(self, tags):

        rows = self.list.GetItemCount()

        for row in range(rows):
            # we only care about the button column, column 1
            item = self.list.GetItem(itemId=row, col=1)

            val_org = item.GetText()

            try:
                val = int(val_org) - 1 # subtract 1 b/c action numbering starts at 1
                action = tags[val].get_name()
                self.list.SetStringItem(row, 2, str(action))
                self.list.SetStringItem(row, 1, str(val_org))

            except Exception as e:
                print e
                continue

    def apply_initiative(self, init_name):

        tags = self.controller.get_tags_by_init(init_name)

        self.apply_tags_to_list(tags)
