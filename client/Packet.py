__author__ = 'sdiemert'

INIT = 0
ACCEPT = 1
GO = 2
DATA = 3
TIME = 4
DONE = 5
TERM = 6

import Data


class Packet:
    def __init__(self):
        self.seq = None
        self.ack = None
        self.type = None
        self.action = None

    def type_name(self):
        if self.type is None:
            return None
        elif self.type == 0:
            return "INIT"
        elif self.type == 1:
            return "ACCEPT"
        elif self.type == 2:
            return "GO"
        elif self.type == 3:
            return "DATA"
        elif self.type == 4:
            return "TIME"
        elif self.type == 5:
            return "DONE"
        elif self.type == 6:
            return "TERM"
        else:
            return None

    def is_term(self):
        if self.type == TERM:
            return True
        else:
            return False

    def is_complete(self):
        if self.seq is None:
            return False
        elif self.action is None:
            return False
        elif self.ack is None:
            return False
        elif self.type is None:
            return False
        else:
            return True

    def is_data_done(self):
        if self.type and self.type == DONE:
            return True
        else:
            return False

    def is_data(self):
        if self.type and self.type == DATA:
            return True
        else:
            return False


class TimePacket(Packet):
    def __init__(self):
        # Call to super class
        Packet.__init__(self)

        self.min = None
        self.hour = None
        self.day = None
        self.month = None
        self.year = None

    def is_complete(self):
        if not Packet.is_complete(self):
            return False
        elif self.min is None:
            return False
        elif self.hour is None:
            return False
        elif self.day is None:
            return False
        elif self.month is None:
            return False
        elif self.year is None:
            return False
        else:
            return True

    def __str__(self):
        s = "< TimedPacket : { "
        s += "seq:" + str(self.seq) + ", "
        s += "ack:" + str(self.ack) + ", "
        s += "type:" + self.type_name() + ", "
        s += "action:" + str(self.action) + ", "
        s += "min:" + str(self.min) + ", "
        s += "hour:" + str(self.hour) + ", "
        s += "day:" + str(self.day) + ", "
        s += "month:" + str(self.month) + ", "
        s += "year:" + str(int(self.year))
        s += " } >"

        return s

    def get_data(self):

        if not self.is_complete():
            return None

        else:
            return Data.Data(self.action, self.min, self.hour, self.day, self.month, self.year)
