from nextcord.ext import commands

from .errors import NotInGuild

__all__ = ("is_manager", "is_moderator", "is_trial_moderator", "is_booster", "community_server_only", "test_server_only")


def is_manager():
    return commands.has_any_role(994927712135286828, 994927785351053362)


def is_moderator():
    return commands.has_any_role(994927712135286828, 994927785351053362, 994928036015259698)


def is_trial_moderator():
    return commands.has_any_role(994927712135286828, 994927785351053362, 994928036015259698, 994928096023154819)


def is_booster():
    return commands.has_any_role(994927712135286828, 994927785351053362, 995608606609252406)


def in_guilds(*guild_ids):
    def predicate(ctx):
        if ctx.guild is None or ctx.guild.id not in guild_ids:
            raise NotInGuild("This command is not available in this guild.")
        return True
    return commands.check(predicate)


def community_server_only():
    return in_guilds(994266247577485473)


def work_servers():
    return in_guilds(994266247577485473, 990272312144183356)