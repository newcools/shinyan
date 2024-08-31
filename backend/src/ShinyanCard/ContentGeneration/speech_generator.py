import io
from openai import OpenAI


def generate_speech(api_key: str, text: str) -> io.BytesIO:
    client = OpenAI(api_key=api_key)

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
