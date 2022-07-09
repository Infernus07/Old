import itertool

import nextcord
from nextcord.ext import commands


class CustomHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(command_attrs={"help": "Show help about the bot, a command, or a category."})

    def make_default_embed(self, cogs):
        embed = nextcord.Embed(
            color=nextcord.Color.blue(),
            description=(
                f"Use `{self.context.clean_prefix}help <command>` for more info on a command.\n"
                f"Use `{self.context.clean_prefix}help <category>` for more info on a category."
            )
        )
        embed.set_author(name=f"{self.context.bot.user.name} Command Categories (Page 1/1)", icon_url=self.context.bot.user.avatar)

        for cog in cogs:
            cog, description, commands = cog
            description = f"{description or 'No Description'} \n {''.join([f'`{command.qualified_name}` ' for command in commands])}"
            embed.add_field(name=cog.qualified_name, value=description, inline=False)

        return embed

    def make_help_embed(self, commands, title, description):
        embed = nextcord.Embed(color=nextcord.Color.blue(), description=description)
        embed.set_author(name=title, icon_url=self.context.bot.user.avatar)
        embed.set_footer(text=f'Use "{self.context.clean_prefix}help command" for more info on a command.')

        for command in commands:
            signature = f"{self.context.clean_prefix}{command.qualified_name} "
            signature += command.signature
            embed.add_field(name=signature, value=command.help or "No help found...", inline=False)

        return embed

    def get_category(self, command):
        cog = command.cog
        return cog.qualified_name if cog else "\u200bNo Category"

    async def send_error_message(self, error):
        await self.context.send(str(error))

    async def send_bot_help(self, mapping):
        filtered = await self.filter_commands(self.context.bot.commands, sort=True, key=self.get_category)
        pages = []

        for cog, commands in itertools.groupby(filtered, key=self.get_category):
            commands = sorted(commands, key=lambda c: c.name)

            if len(commands) == 0:
                continue

            cog = self.context.bot.get_cog(cog)
            description = (cog and cog.description) if (cog and cog.description) else nextcord.Embed.Empty

            pages.append((cog, description, commands))

        cogs = pages[
            min(len(pages) - 1, 0) : min(len(pages) - 1, 6)
        ]

        embed = self.make_default_embed(cogs)
        await self.context.send(embed=embed)

    async def send_cog_help(self, cog):
        filtered = await self.filter_commands(cog.get_commands(), sort=True)

        embed = self.make_help_embed(filtered, title=(cog and cog.qualified_name or "Other") + " Commands", description=cog.description if cog else nextcord.Embed.Empty)
        await self.context.send(embed=embed)

    async def send_group_help(self, group):
        subcommands = group.commands
        if len(subcommands) == 0:
            return await self.send_command_help(group)

        filtered = await self.filter_commands(subcommands, sort=True)

        embed = self.make_help_embed(filtered, title=group.qualified_name.title(), description=f"{group.description}\n\n{group.help}" if group.description else group.help or "No help found...")
        await self.context.send(embed=embed)

    async def send_command_help(self, command):
        embed = nextcord.Embed(
            color=nextcord.Color.blue(),
            title=f"{self.context.clean_prefix}{command.qualified_name}",
            description=f"{command.description}\n\n{command.help}" if command.description else command.help or "No help found..."
        )
        embed.add_field(name="Signature", value=self.get_command_signature(command))
        await self.context.send(embed=embed)

def setup(bot):
    bot.old_help_command = bot.help_command
    bot.help_command = CustomHelpCommand()

def teardown(bot):
    bot.help_command = bot.old_help_command