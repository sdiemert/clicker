__author__ = 'sdiemert'

class Controller:

    def __init__(self, view=None):
        """
        :param view:AppFrame
        :return:Controller
        """

        self.view = view

    def set_view(self, view):
        self.view = view

    def _view_message(self, s):
        if not self.view:
            raise RuntimeError("Controller does not have a view linked to it, cannot send it a message.")
        else:
            self.view.display_message(s)

    def upload(self, source):
        print "Controller.upload(source='"+source+"')"
        self._view_message("Foobar!")
