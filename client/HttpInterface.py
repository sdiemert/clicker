__author__ = 'sdiemert'

class HttpInterface:

    def __init__(self, host=None, port=None):

        self.host = host
        self.port = port

    def send_data(self, user="", passwd="", data=[]):
        pass