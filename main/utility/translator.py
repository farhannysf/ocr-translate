from googletrans import Translator

translator = Translator()


async def translate(text):
    translation = translator.translate(text)
    return translation.text