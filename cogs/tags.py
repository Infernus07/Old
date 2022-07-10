import plasma

import nextcord
from nextcord.ext import commands


class Tags(commands.Cog):
    """For tags."""

    def __init__(self, bot):
        self.bot = bot

    def has_profanity(self, *, content=None, name=None):
        if content is not None:
            words = content.split()
            for i in plasma.BANNED_WORDS:
                if any(i in x for x in words):
                    return True

        if name is not None:
            words = name.split()
            for i in plasma.BANNED_WORDS:
                if any(i in x for x in words):
                    return True

        return False