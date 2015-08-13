__author__ = 'sdiemert'

class Controller:

    def __init__(self, view=None):
        self.view = view

    def set_view(self, view):
        self.view = view

    def upload(self, source):
        print "Controller.upload()"
        self.view.display_message("Foobar!")
