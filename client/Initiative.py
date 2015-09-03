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


class Initiative(Entity):
    def __init__(self, iid="", name="", tags=[]):
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

    def __repr__(self):
        return "Initiative { id: " + str(self.id) + ", name: " + self.name + ", tags: " + str(self.tags) + " }"
