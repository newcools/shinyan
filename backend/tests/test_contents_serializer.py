import json

from src.ShinyanCard.CardContents import CardContents, ContentItem, ContentItemResource, ContentType, \
    serialize_card_contents, deserialize_card_contents


class TestContentsSerializer:
    def test_content_serializer_deserializer(self):
        # Sample data
        card_contents = CardContents(
            name="Learning Cards",
            key="learning-cards",
            contents=[
                ContentItem(
                    value="Learn Japanese",
                    extra={"difficulty": "easy"},
                    resources=[
                        ContentItemResource(type=ContentType.AUDIO, uri="http://example.com/audio.mp3",
                                            extra={"duration": 120}),
                        ContentItemResource(type=ContentType.IMAGE, uri="http://example.com/image.png",
                                            extra={"size": "1024x768"})
                    ]
                )
            ]
        )

        # Serialize
        serialized_data = serialize_card_contents(card_contents)

        # Deserialize back to Python objects
        json_data = json.loads(serialized_data)  # Load JSON string to dict
        deserialized_card_contents = deserialize_card_contents(json_data)

        assert card_contents == deserialized_card_contents

