import enum
from datetime import datetime


class StorableType(enum.Enum):
    DIRECTORY = 1
    TEXT = 2
    MULTI_MEDIA = 3


class Storable:
    def __init__(self, _id, _name="", _type=StorableType.TEXT, _children=None, _size=0, _modified_at=None):
        if _children is None:
            _children = []
        self.type = _type
        self.id = _id
        self.size = _size
        self.modified_at = datetime.strptime(_modified_at, "%Y-%m-%d") if _modified_at else None
        self.name = _name
        self.children = _children
