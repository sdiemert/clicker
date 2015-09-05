__author__ = 'sdiemert'


class Entity:
    def __init__(self, eid="", name=""):
        self.id = eid
        self.name = name

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

class Tag(Entity):
    def __init__(self, tid="", name="", value=0):
        """
        :param iid: String
        :param name: String
        :param value: Integer
        :return:
        """
        Entity.__init__(self, tid, name)
        self.value = value

    def __repr__(self):
        return "Tag { id: "+ str(self.id)+", name: "+str(self.name)+", value: "+str(self.value)+" }"

class Initiative(Entity):
    def __init__(self, iid="", name="", tags=list()):
        """
        :param id:  String
        :param name: String
        :param tags: List
        :return:
        """
        Entity.__init__(self, iid, name)
        self.tags = tags

    def get_tags(self):
        return self.tags

    def add_tag(self, s):
        self.tags.append(s)

    def __repr__(self):
        return "Initiative { id: " + str(self.id) + ", name: " + self.name + ", tags: " + str(self.tags) + " }"
