__author__ = 'sdiemert'

from Initiative import Entity

class Member(Entity):

    def __init__(self, mid, name, city, province):
        Entity.__init__(self, mid, name)
        self.city = city
        self.province = province

    def __repr__(self):
        return "Member { id: "+str(self.id)+", name: "+str(self.name)+", city: "+str(self.city)+", province: "+str(self.province)+" }"
