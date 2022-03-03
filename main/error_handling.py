from discord.ext import commands
from aiohttp.client_exceptions import ClientConnectorError
from utility.message_formatting import embify, get_argument_value
from settings import commands_config, MAINTAINER_ID


async def internal_error(ctx):
    return await ctx.send(
        f"An internal error has occured, please contact <@!{MAINTAINER_ID}>."
    )


async def translate_command_error(ctx, error):
    parameter = commands_config["translate"]["parameters"][0]
    argument_attributes = parameter["arguments"]
    parameter_name = parameter["name"]
    argument_value = await get_argument_value(argument_attributes)
    helper_text = "Use `!ocr-help` for usage guide."

    if isinstance(error, commands.MissingRequiredArgument):
        title = "Error: Missing Required Argument"
        description = f"Required argument: `{parameter_name}`.\n\nExpected `{parameter_name}` arguments:\n{argument_value}\n\n{helper_text}"
        embed = await embify(title, description)
        return await ctx.send(embed=embed)

    elif isinstance(error, commands.BadArgument):
        title = "Error: Bad Argument"
        description = f"Invalid `{parameter_name}` argument provided.\n\nExpected `{parameter_name}` arguments:\n{argument_value}\n\n{helper_text}"
        embed = await embify(title, description)
        return await ctx.send(embed=embed)

    elif isinstance(error, commands.ArgumentParsingError):
        title = f"Error: {error.args[0]}"

        if error.args[0] == "No Image":
            description = (
                f"No image file attached or URL to image provided.\n\n{helper_text}"
            )
            embed = await embify(title, description)
            return await ctx.send(embed=embed)

        if error.args[0] == "No Text":
            description = (
                f"No text detected within the provided image.\n\n{helper_text}"
            )
            embed = await embify(title, description)
            return await ctx.send(embed=embed)

        if error.args[0] == "Invalid Filetype":
            description = f"Invalid file type provided.\n\n(File type provided: {error.args[1]})\n\n{helper_text}"
            embed = await embify(title, description)
            return await ctx.send(embed=embed)

        if error.args[0] == "Image File and URL Exist":
            description = f"Cannot have both attached image file and URL to image in the same time.\n\n{helper_text}"
            embed = await embify(title, description)
            return await ctx.send(embed=embed)

        if error.args[0] == "Excess Image File":
            description = f"Cannot have more than 1 attached image file in the same time.\n\n{helper_text}"
            embed = await embify(title, description)
            return await ctx.send(embed=embed)

        if error.args[0] == "Excess URL":
            description = (
                f"Cannot have more than 1 URL in the same time.\n\n{helper_text}"
            )
            embed = await embify(title, description)
            return await ctx.send(embed=embed)

        if error.args[0] == "Connection Failed":
            if error.args[1] == "Image Read":
                description = f"Unable to read image, failed to get resource from the provided image URL.\n\n(Reason: {error.args[2]})"
                embed = await embify(title, description)
                return await ctx.send(embed=embed)

    else:
        if isinstance(error.original, ClientConnectorError):
            title = "Error: No Connection"
            description = f"Cannot establish connection to the provided image URL."
            embed = await embify(title, description)
            return await ctx.send(embed=embed)

        return await internal_error(ctx)