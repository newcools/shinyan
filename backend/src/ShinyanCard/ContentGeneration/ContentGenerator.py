import json

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from ..Settings import settings


def prompt_for_japanese(word, translation="english"):
    return f"""
        Please give me a few simple example sentences of the Japanese word {word}
        and use the most commonly used words. Also, add the hiragana next to each sentence plus its {translation} translation.
        The sentence must be complete and not overly simple, with at least 10 words.
        Please provide the response in a JSON format which has a list of objects that have 3 properties using camel case, 
        text(japanese), hiragana, and translation ({translation}).
        The list must be under a root called 'contents'.
    """


def prompt_for_chinese(word, translation="english"):
    return f"""
        Please give me a few simple example sentences of the Chinese word {word}
        and use the most commonly used words. Also, add the pin yin next to each sentence plus its {translation} translation.
        The sentence must be complete and not overly simple, with at least 10 words.
        Please provide the response in a JSON format which has a list of objects that have 3 properties using camel case,
        text(chinese), pinyin, and translation ({translation}), which is the translation.
        The list must be under a root called 'contents'.
    """


def generate_contents(word, language="chinese"):
    """Generates sentences for a given word and saves the output to a file.

    Args:
        word: The word to generate sentences for.
        language: the language it uses
    """
    prompt_template = ""
    if language == "chinese":
        prompt_template = prompt_for_chinese(word)
    elif language == "japanese":
        prompt_template = prompt_for_japanese(word)
    else:
        raise ValueError(f"Language '{language}' is not supported.")

    prompt = PromptTemplate.from_template(template=prompt_template)
    prompt_formatted_str = prompt.format(word=word)

    llm = ChatOpenAI(
        api_key=settings.openai.api_key,
        response_format={"type": "json_object"},
        model="gpt-4o-mini",
    )
    response = llm.invoke(prompt_formatted_str)
    content_data = json.loads(response.content)

    # examples_items = examples_data['examples']
    # if len(examples_items) > 1:
    #     index = random.randint(0, len(examples_items) - 1)
    #     example = examples_items[index]
    #     audio_path = Path(current_card.key) / str(index) / 'audio.mp3'
    #     audio = azure_blob_sync.pull(audio_path.as_posix())
    #     if audio is None:
    #         audio = generate_speech(settings.openai.api_key.get_secret_value(), example['Japanese'])
    #         azure_blob_sync.push(audio_path.as_posix(), audio)
    #     download_link = azure_blob_sync.get_download_link(audio_path.as_posix())
    #     print(download_link)
    #     print(example['English'])
    #     print(example['Japanese'])
    #     print(example['Hiragana'])

    return content_data

