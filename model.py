import enum


class StorableType(enum.Enum):
    DIRECTORY = 1
    FILE = 2


class Storable:
    def __init__(self, data: dict, parent=None):
        self.type = data.get("type", None)
        self.id = data.get("id", None)
        self.size = data.get("size", None)
        self.modified_at = data.get("modified_at", None)
        self.name = data.get("name", None)
        self.parent = parent
        self.children = list(map(lambda x: Storable(x, self), data.get("children", [])))

    def isDir(self):
        return self.type == StorableType.DIRECTORY.value




class User:
    def __init__(self, data: dict):
        self.id = data.get("id", None)
        self.fullname = data.get("fullname", None)
        self.email = data.get("email", None)
        self.root = Storable(data.get("root"))
