import enum


class MessageType(enum.Enum):
    TEXT = "TEXT"
    AUDIO = "AUDIO"
    IMAGE = "IMAGE"
    FILE = "FILE"


class MessageStatus(enum.Enum):
    SENT = "SENT"
    DELIVERED = "DELIVERED"
    READ = "READ"
