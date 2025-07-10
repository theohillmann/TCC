from enum import Enum, auto


class MessageType(Enum):
    TEXT = auto()
    AUDIO = auto()
    UNKNOWN = auto()
