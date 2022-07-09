from nextcord.ext import commands

__all__ = (
    "NotInGuild",
)


class NotInGuild(commands.CheckFailure):
    pass