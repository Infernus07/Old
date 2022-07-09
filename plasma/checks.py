from nextcord.ext import commands

from .errors import NotInGuild


def in_guilds(*guild_ids):
    def predicate(ctx):
        if ctx.guild is None or ctx.guild.id not in guild_ids:
            raise NotInGuild("This command is not available in this guild.")
        return True
    return commands.check(predicate)


def community_server_only():
    return in_guilds(994266247577485473)