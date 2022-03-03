import re
from discord.ext.commands import ArgumentParsingError
from utility.ocr import execute_ocr
from utility import translator
from utility.regex import url_syntax
from utility.message_formatting import split_messages


async def logic(ctx, ocrType):
    url = re.findall(url_syntax, ctx.message.content)
    if ctx.message.attachments == [] and url == []:
        raise ArgumentParsingError(message="No Image")

    if ctx.message.attachments and url:
        raise ArgumentParsingError(message="Image File and URL Exist")

    if ctx.message.attachments:
        attachments_filetype = ctx.message.attachments[0].content_type.split("/")[0]
        if attachments_filetype != "image":
            raise ArgumentParsingError(message="Invalid Filetype")

        if len(ctx.message.attachments) > 1:
            raise ArgumentParsingError(message="Excess Image File")

        image_url = ctx.message.attachments[0].url

    elif url:
        if len(url) > 1:
            raise ArgumentParsingError(message="Excess URL")

        image_url = url[0]
        if image_url[0:4] != "http":
            image_url = "http://" + image_url

    ocr_text, language = await execute_ocr(image_url, ocrType)
    textType = "OCR Result"
    await split_messages(ctx, ocr_text, textType, limit=2000)
    if language == "en":
        return

    translated_text = await translator.translate(ocr_text)
    textType = f"OCR Translation"
    return await split_messages(ctx, translated_text, textType, limit=2000)