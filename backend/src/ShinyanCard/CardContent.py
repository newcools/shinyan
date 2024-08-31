from dataclasses import dataclass, field
from typing import List
from enum import Enum

class ContentType(Enum):
    AUDIO = "audio"
    VIDEO = "video"
    IMAGE = "image"
    TEXT = "text"

@dataclass
class ContentItem:
    type: ContentType
    link: str
    description: str

@dataclass
class CardContents:
    name: str
    key: str
    contents: List[ContentItem] = field(default_factory=list)
