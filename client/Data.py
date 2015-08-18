__author__ = 'sdiemert'

class Data:

    def __init__(self, action=None, min=None, hour=None, day=None, month=None, year=None):

        self.action = action
        self.min = min
        self.hour = hour
        self.day = day
        self.month = month
        self.year = year

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

    def __str__(self):

        s = "< Data : { "
        s += "action:"+str(self.action)+", "
        s += "min:"+str(self.min)+", "
        s += "hour:"+str(self.hour)+", "
        s += "day:"+str(self.day)+", "
        s += "month:"+str(self.month)+", "
        s += "year:"+str(self.year)+", "
        s += " } >"

        return s
