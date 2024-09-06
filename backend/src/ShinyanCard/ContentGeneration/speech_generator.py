import io
from openai import OpenAI
from ..Settings import settings


def generate_speech(text: str) -> io.BytesIO:
    client = OpenAI(api_key=settings.openai.api_key)

    with client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="shimmer",
            input=text,
            response_format='mp3'
    ) as response:
        binary_stream = io.BytesIO()

        for chunk in response.iter_bytes(chunk_size=8192):
            if chunk:
                binary_stream.write(chunk)

        binary_stream.seek(0)
        return binary_stream
