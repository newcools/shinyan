import json
from dataclasses import asdict, dataclass, field
from typing import List
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
    extra: object

@dataclass
class ContentItem:
    value: str
    extra: object
    resources: List[ContentItemResource] = field(default_factory=list)

@dataclass
class CardContents:
    name: str
    key: str
    contents: List[ContentItem] = field(default_factory=list)


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        if hasattr(obj, '__dict__'):
            return asdict(obj)
        return super().default(obj)


def deserialize_card_contents(json_data: dict) -> CardContents:
    def content_type_decoder(content_type_str):
        return ContentType(content_type_str)

    def content_item_resource_decoder(resource_data):
        return ContentItemResource(
            type=content_type_decoder(resource_data['type']),
            uri=resource_data['uri'],
            extra=resource_data.get('extra', None)
        )

    def content_item_decoder(content_data):
        return ContentItem(
            value=content_data.get('value', None),
            extra=content_data.get('extra', None),
            resources=[content_item_resource_decoder(res) for res in content_data.get('resources', [])]
        )

    name = json_data.get('name', None)
    key = json_data.get('key', None)
    contents = [content_item_decoder(item) for item in json_data.get('contents', [])]

    return CardContents(
        name=name,
        key=key,
        contents=contents
    )

def serialize_card_contents(card_contents: CardContents) -> str:
    return json.dumps(asdict(card_contents), cls=CustomJSONEncoder)
