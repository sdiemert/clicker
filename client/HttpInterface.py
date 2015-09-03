__author__ = 'sdiemert'

import httplib

class HttpInterface:

    def __init__(self, host=None, port=None):

        self.host = host
        self.port = port

    def send_data(self, user="", passwd="", data=[]):
        pass

