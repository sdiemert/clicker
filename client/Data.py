__author__ = 'sdiemert'

from datetime import date
import time

class Data:

    def __init__(self, action=None, min=None, hour=None, day=None, month=None, year=None):

        self.action = action
        self.min = min
        self.hour = hour
        self.day = day
        self.month = month
        self.year = year

        self.initiative = None
        self.tag = None
        self.user = None

    def is_complete(self):

        if not self.action:
            return False
        elif not self.min:
            return False
        elif not self.hour:
            return False
        elif not self.day:
            return False
        elif not self.month:
            return False
        elif not self.year:
            return False
        else:
            return True

    def get_list_rep(self):

        d = date(self.year, self.month, self.day)

        return (str(self.action), str(d.isoformat()))

    def getUTCSeconds(self):
        d = date(int(self.year), int(self.month), int(self.day))
        return int(time.mktime(d.timetuple()))

    def __str__(self):

        s = "< Data : { "
        s += "action:"+str(self.action)+", "
        s += "init:"+str(self.initiative)+", "
        s += "tag:"+str(self.tag)+", "
        s += "username:"+str(self.tag)+", "
        s += "min:"+str(self.min)+", "
        s += "hour:"+str(self.hour)+", "
        s += "day:"+str(self.day)+", "
        s += "month:"+str(self.month)+", "
        s += "year:"+str(self.year)+", "
        s += " } >"

        return s
