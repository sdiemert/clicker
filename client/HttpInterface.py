__author__ = 'sdiemert'

import httplib

class HttpInterface:
    def __init__(self, host=None, port=None, timeout=5):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.conn = None

    def get_request(self, route):

        try:
            self.conn = httplib.HTTPConnection(self.host, self.port, timeout=self.timeout)

            self.conn.request("GET", route)

            r = self.conn.getresponse()

            if r.status != 200:
                print "Got status code: "+str(r.status)
                self.conn.close()
                return None
            else:
                x = r.read()
                self.conn.close()
                return x

        except Exception as e:
            print e
            print "Could not connect to: "+ str(self.host)+ " on port: "+str(self.port)
            return None

    def send_data(self, user="", passwd="", data=[]):
        pass

    def set_host(self, h):
        self.host = h

    def set_port(self, p):
        self.port = p

    def _precondition(self):
        if not self.host or not self.port:
            return False
        else:
            return True

    def check_remote(self):

        if not self._precondition():
            return False

        if self.get_request("/status"):
            return True
        else:
            return False

    def fetch_initiatives(self):

        return self.get_request("/initiatives")

    def fetch_members(self):

        return self.get_request("/members")

    def __repr__(self):
        return "HttpInterface { host : " + str(self.host) + ", port : " + str(self.port) + " }"


if __name__ == "__main__":

    h = HttpInterface('localhost', 3000)

    print h.fetch_initiatives()
