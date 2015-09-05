__author__ = 'sdiemert'

import httplib
import json
from Initiative import Initiative
from Initiative import Tag
from Member import Member
import pprint


pp = pprint.PrettyPrinter(indent=4)

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
                x = json.loads(x)
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

        inits = self.get_request("/initiatives")

        toReturn = []

        for i in inits:

            tmpInit = Initiative(str(i), str(inits[i]['name']), tags=list())

            for t in inits[i]['tags']:
                tmpInit.add_tag(Tag(str(t['_id']), str(t['name'])))

            toReturn.append(tmpInit)

        return toReturn

    def fetch_members(self):

        members =  self.get_request("/members")

        toReturn = list()

        for m in members:
            toReturn.append(Member(m['_id'], m['name'], m['city'], m['province']))

        return toReturn


    def __repr__(self):
        return "HttpInterface { host : " + str(self.host) + ", port : " + str(self.port) + " }"


if __name__ == "__main__":

    h = HttpInterface('localhost', 3000)

    #pp.pprint(h.fetch_initiatives())
    pp.pprint(h.fetch_members())
