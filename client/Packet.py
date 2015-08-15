__author__ = 'sdiemert'

INIT = 0
ACCEPT = 1
GO = 2
DATA = 3
TIME = 4
DONE = 5
TERM = 6


class Packet:
    def __init__(self):
        self.seq = None
        self.ack = None
        self.type = None

    def is_term(self):
        if self.type == TERM:
            return True
        else:
            return False

    def is_complete(self):
        if self.seq is None:
            return False
        elif self.ack is None:
            return False
        elif self.type is None:
            return False
        else:
            return True


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
        s += "type:" + str(self.type) + ", "
        s += "min:" + str(self.min) + ", "
        s += "hour:" + str(self.hour) + ", "
        s += "day:" + str(self.day) + ", "
        s += "month:" + str(self.month) + ", "
        s += "year:" + str(int(self.year))
        s += " } >"

        return s
