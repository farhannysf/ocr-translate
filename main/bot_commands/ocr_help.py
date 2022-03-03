from settings import commands_config
from utility.message_formatting import HelpMessage


async def logic(ctx):
    command_description = (
        "This bot extracts text from image and translate it to English."
    )

    usage_description = "To use, upload and attach an image to the command message or provide URL to image."
    translate_command = commands_config["translate"]
    help_message = HelpMessage(
        command_description, usage_description, translate_command
    )

    embed = await help_message.format()

    return await ctx.send(embed=embed)