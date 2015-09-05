__author__ = 'sdiemert'

from SerialInterface import SerialInterface
from HttpInterface import HttpInterface
import ConfigParser as cp

class Controller:

    def __init__(self, view=None):
        """
        :param view:AppFrame
        :return:Controller
        """

        self.view = view
        self.serial = SerialInterface(view=self.view)
        self.data = []
        self.initiatives = []
        self.members = []
        self.http = HttpInterface()
        self.conf = None

    def set_view(self, view):
        self.view = view
        self.serial.set_view(view)

    def get_interfaces(self):
        if not self.serial:
            return []
        else:
            return self.serial.get_available_serial_ports()

    def get_initiatives(self):
        return [i.get_name() for i in self.initiatives]

    def get_members(self):
        return [i.get_name() for i in self.members]

    def set_initiatives(self, inits):
        self.initiatives = inits

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
        self.initiatives = []
        self.serial.reset()

    def init(self):
        """
        Initializes the application logic:
        1) Checks that remote host for web server is available
        2) Fetches and stores current initiatives and tags from remote web server
        3) Other?
        :return: True if all checks and setup pass, False otherwise.
        """

        # Load the remote host info from the config file

        self.conf = cp.ConfigParser()
        self.conf.read('config.ini')
        self.http.set_host(str(self.conf.get('remotehost', 'hostname')))
        self.http.set_port(str(self.conf.get('remotehost', 'port')))

        print "http interface is configured to: " + str(self.http)

        # Check that the remote host can be connected to.

        if not self.http.check_remote():
            raise Exception("Could not contact server at: "+str(self.http.host) + " on port: "+str(self.http.port))

        # Fetch initiatives and tags from remote host

        self.initiatives = self.http.fetch_initiatives()
        self.members = self.http.fetch_members()

    def show_data(self):

        d = self.serial.get_data()

        if d:
            self._view_message("Data is: ")
            for i in d:
                self._view_message(str(i))
