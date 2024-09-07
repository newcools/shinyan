import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum

# Enum and Data Classes
class ContentType(Enum):
    AUDIO = "audio"
    VIDEO = "video"
    IMAGE = "image"
    TEXT = "text"


@dataclass
class ContentItemResource:
    type: ContentType
    uri: str
    extra: Optional[object] = None

@dataclass
class BaseContentItem:
    text: Optional[str] = None
    translation: Optional[str] = None
    extra: Optional[object] = None
    resources: List[ContentItemResource] = field(default_factory=list)

@dataclass
class CardContents:
    name: Optional[str] = None
    key: Optional[str] = None
    contents: List[BaseContentItem] = field(default_factory=list)

@dataclass
class JapaneseContentItem(BaseContentItem):
    hiragana: Optional[str] = None

@dataclass
class MandarinContentItem(BaseContentItem):
    pinyin: Optional[str] = None

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, (ContentItemResource, BaseContentItem, CardContents, JapaneseContentItem, MandarinContentItem)):
            return obj.__dict__
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def custom_decoder(dct):
    if 'type' in dct and isinstance(dct['type'], str):
        dct['type'] = ContentType(dct['type'])  # Convert to ContentType Enum if present

    if 'hiragana' in dct:  # JapaneseContentItem
        return JapaneseContentItem(
            text=dct.get('text'),
            translation=dct.get('translation'),
            extra=dct.get('extra'),
            resources=[custom_decoder(res) for res in dct.get('resources', [])],
            hiragana=dct.get('hiragana')
        )
    elif 'pinyin' in dct:  # MandarinContentItem
        return MandarinContentItem(
            text=dct.get('text'),
            translation=dct.get('translation'),
            extra=dct.get('extra'),
            resources=[custom_decoder(res) for res in dct.get('resources', [])],
            pinyin=dct.get('pinyin')
        )
    elif 'uri' in dct:  # ContentItemResource
        return ContentItemResource(
            type=dct.get('type'),
            uri=dct.get('uri'),
            extra=dct.get('extra')
        )
    elif 'contents' in dct:
        return CardContents(
            name=dct.get('name'),
            key=dct.get('key'),
            contents=[custom_decoder(item) for item in dct.get('contents', [])]
        )
    else:  # BaseContentItem
        return BaseContentItem(
            text=dct.get('text'),
            translation=dct.get('translation'),
            extra=dct.get('extra'),
            resources=[custom_decoder(res) for res in dct.get('resources', [])]
        )
