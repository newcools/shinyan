import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from .. import CardContent
from ..Settings import settings


def prompt_for_japanese(word):
    return """
        Please give me a few simple example sentences of the Japanese word {word}
        and use the most commonly used words. Also, add the hiragana next to each sentence plus its English translation.
        The sentence must be complete and not overly simple, with at least 10 words.
        Please provide the response in a JSON format which has a list of objects that have 3 properties, 
        Japanese, Hiragana, and English, which is the translation.
    """


def prompt_for_chinese(word):
    return """
        Please give me a few simple example sentences of the Chinese word {word}
        and use the most commonly used words. Also, add the hiragana next to each sentence plus its English translation.
        The sentence must be complete and not overly simple, with at least 10 words.
        Please provide the response in a JSON format which has a list of objects that have 3 properties, 
        Japanese, Pin Ying, and English, which is the translation.
    """


def generate_contents(word, language="chinese") -> CardContent:
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
        api_key=settings.openai_key.get_secret_value(),
        response_format={"type": "json_object"},
        model="gpt-4o-mini",
    )
    response = llm.invoke(prompt_formatted_str)
    gen_sentences = json.loads(response.content)
    content = CardContent()
    return content

