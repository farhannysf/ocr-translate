import logging
import discord
import bot_commands
import error_handling
from discord.ext import commands
from settings import BOT_NAME, BOT_TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = commands.Bot(command_prefix="!ocr-", help_command=None)


@client.event
async def on_ready():
    logger.info(f"{BOT_NAME} running as {client.user.name} ({client.user.id}).\n------")
    activity = discord.Game("!ocr-translate")
    await client.change_presence(status=discord.Status.online, activity=activity)


@client.command(pass_context=True)
async def translate(ctx, ocrType: str):
    if ocrType == "text" or ocrType == "document":
        await bot_commands.ocr_translate.logic(ctx, ocrType)

    else:
        raise discord.ext.commands.BadArgument


@translate.error
async def translate_error(ctx, error):
    logger.error({"command": "translate", "error": error})
    return await error_handling.translate_command_error(ctx, error)


@client.command(pass_context=True)
async def help(ctx):
    await bot_commands.ocr_help.logic(ctx)


@help.error
async def help_error(ctx, error):
    logger.error({"command": "translate", "error": error})
    return await error_handling.internal_error(ctx)


if __name__ == "__main__":
    client.run(BOT_TOKEN)
    logger.critical("Client Event Loop Exit")