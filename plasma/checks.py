from nextcord.ext import commands

from .errors import NotInGuild

__all__ = (
    "in_guilds",
    "community_server_only"
)


def is_manager():
    return commands.has_any_role(994927712135286828, 994927785351053362)


def is_moderator():
    return commands.has_any_role(994927712135286828, 994927785351053362, 994928036015259698)


def is_trial_moderator():
    return commands.has_any_role(994927712135286828, 994927785351053362, 994928036015259698, 994928096023154819)


def in_guilds(*guild_ids):
    def predicate(ctx):
        if ctx.guild is None or ctx.guild.id not in guild_ids:
            raise NotInGuild("This command is not available in this guild.")
        return True
    return commands.check(predicate)


def community_server_only():
    return in_guilds(994266247577485473)