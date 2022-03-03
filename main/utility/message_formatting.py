from discord import Embed
from settings import MAINTAINER_ID


async def bounded_split(message, limit=2000):
    paragraphs = []
    lines = iter(message.splitlines())
    current = next(lines)

    for line in lines:
        if len(current) + len(line) >= limit:
            paragraphs.append(current)
            current = line
        else:
            current += "\n" + line

    paragraphs.append(current)

    return paragraphs


async def split_messages(ctx, text, textType, limit):
    paragraphs = await bounded_split(text, limit)
    if len(paragraphs) > 1:
        for i, splice in enumerate(paragraphs):
            title = f"{textType}\n\nPart {i+1}"
            description = splice
            embed = await embify(title, description)
            await ctx.send(embed=embed)
    else:
        title = textType
        description = paragraphs[0]
        embed = await embify(title, description)
        await ctx.send(embed=embed)

    return


async def embify(title, description):
    embed = Embed(title=title, description=description, color=0xE74C3C)

    return embed


async def get_argument_value(argument_attributes):
    argument_value = "\n".join(
        f"`{attribute['value']}`" for attribute in argument_attributes
    )
    return argument_value


class HelpMessage:
    def __init__(self, command_description, usage_description, command):
        self.command_description = command_description
        self.usage_description = usage_description

        self.command = command
        self.parameters = command.get("parameters")

    string_tail = "\n------"

    async def create_description(self):
        title = "Usage Guide"
        description_message = f"{self.command_description}\n\n{self.usage_description}"
        embed = await embify(title, description_message)
        return embed

    async def format(self):
        embed = await self.create_description()
        command_syntax = f"`{self.command['syntax']}`"
        if self.parameters == None:
            embed.add_field(name="Command:", value=command_syntax + self.string_tail)
            return embed

        command_parameters = [parameters for parameters in self.parameters]
        parameters_values = " ".join(
            "`{}`".format(parameter["name"]) for parameter in command_parameters
        )

        command_message = f"{command_syntax} {parameters_values}"
        embed.add_field(name="Command:", value=command_message + self.string_tail)
        await self.populate_fields("argument_value", embed)
        await self.populate_fields("argument_description", embed)
        maintainer_discord = f"<@!{MAINTAINER_ID}>"
        embed.add_field(name="Bot maintainer:", value=maintainer_discord, inline=False)

        return embed

    async def populate_fields(self, field_type, embed):
        for parameter in self.parameters:
            argument_attributes = [attributes for attributes in parameter["arguments"]]
            if field_type == "argument_value":
                argument_value = await get_argument_value(argument_attributes)
                embed.add_field(
                    name=f"{parameter['name']} arguments:",
                    value=argument_value + self.string_tail,
                )

            if field_type == "argument_description":
                argument_description = "\n\n".join(
                    f"`{attribute['value']}`\n{attribute['description']}"
                    for attribute in argument_attributes
                )
                embed.add_field(
                    name=f"{parameter['name']} argument description:",
                    value=argument_description + self.string_tail,
                    inline=False,
                )