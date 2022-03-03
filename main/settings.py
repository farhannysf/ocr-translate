from os import environ

MAINTAINER_ID = environ["MAINTAINER_ID"]
BOT_NAME = environ["BOT_NAME"]
BOT_TOKEN = environ["BOT_TOKEN"]
GOOGLE_VISION_KEY = environ["GOOGLE_VISION_KEY"]

commands_config = {
    "translate": {
        "syntax": "!ocr-translate",
        "parameters": [
            {
                "name": "OCR type",
                "arguments": [
                    {
                        "value": "text",
                        "description": "Optimized to extract short text from image, such as signs.\n\nYou can provide a cropped image from your device screen clipping tool that shows a short text and use this OCR type argument for best OCR accuracy result.",
                    },
                    {
                        "value": "document",
                        "description": "Optimized to extract dense text from image, such as documents.\n\nUse this OCR type argument when extracting text from an image of a document for best OCR accuracy result.",
                    },
                ],
            },
        ],
    }
}