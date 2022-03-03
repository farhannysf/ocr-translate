import base64
import json
from discord.ext.commands import ArgumentParsingError
from utility import rest
from settings import GOOGLE_VISION_KEY


async def read_image(image_url):
    image_response = await rest.asyncGet(image_url)
    if isinstance(image_response, dict):
        if image_response["status"] == "failed":
            raise ArgumentParsingError(
                "Connection Failed", "Image Read", image_response["reason"]
            )

    content_type = image_response.content_type
    if content_type.split("/")[0] != "image":
        raise ArgumentParsingError("Invalid Filetype", content_type)

    image_data = image_response.body

    return base64.b64encode(image_data).decode("UTF-8")


async def post_google_vision(image, ocrType):
    typeOptions = {"text": "TEXT_DETECTION", "document": "DOCUMENT_TEXT_DETECTION"}
    ocrType = typeOptions[ocrType]
    data = {}
    data["requests"] = [
        {
            "image": {"content": image},
            "features": [{"type": ocrType}],
        }
    ]

    json_data = json.dumps(data)
    params = {"key": GOOGLE_VISION_KEY}
    r = await rest.asyncPost(
        "https://vision.googleapis.com/v1/images:annotate?",
        params=params,
        data=json_data,
    )
    return await r.json()


async def execute_ocr(image_url, ocrType):
    image = await read_image(image_url)
    google_vision_json = await post_google_vision(image, ocrType)
    if google_vision_json["responses"] == [{}]:
        raise ArgumentParsingError("No Text")

    language = google_vision_json["responses"][0]["textAnnotations"][0]["locale"]
    text = google_vision_json["responses"][0]["textAnnotations"][0]["description"]
    return text, language