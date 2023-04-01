import enum


class StorableType(enum.Enum):
    DIRECTORY = 1
    TEXT = 2
    MULTI_MEDIA = 3


class Storable:
    def __init__(self, _id, name="", _type=StorableType.TEXT, children=[]):
        self.type = _type
        self.id = _id
        self.name = name
        self.children = children
