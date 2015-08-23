__author__ = 'sdiemert'

from SerialInterface import SerialInterface

class Controller:

    def __init__(self, view=None):
        """
        :param view:AppFrame
        :return:Controller
        """

        self.view = view
        self.serial = SerialInterface(view=self.view)
        self.data = []

    def set_view(self, view):
        self.view = view
        self.serial.set_view(view)

    def get_interfaces(self):
        if not self.serial:
            return []
        else:
            return self.serial.get_available_serial_ports()

    def _view_message(self, s, level=1):
        if not self.view:
            raise RuntimeError("Controller does not have a view linked to it, cannot send it a message.")
        else:
            self.view.display_message(s, level)

    def upload(self, source):
        print "Controller.upload(source='"+source+"')"
        self._view_message("Attempting to gather data from the arduino")

        result = self.serial.connect(source)

        self._view_message("===========================")

        if not result:
            self._view_message("Failed to gather data from Arduino.", 2)
        else:
            self._view_message("Successfully gathered data from Arduino")

        return result

    def reset(self):
        self.data = []
        self.serial.reset()

    def show_data(self):

        d = self.serial.get_data()

        if d:
            self._view_message("Data is: ")
            for i in d:
                self._view_message(str(i))
