import re
import unicodedata

from nextcord.ext import commands

LAST_RESORT = "User"
URL_REGEX   = re.compile(r"(([a-z]{3,6}://)|(^|\s))([a-zA-Z0-9\-]+\.)+[a-z]{2,13}[\.\?\=\&\%\/\w\-]*\b([^@]|$)")


class Names(commands.Cog):
    """For normalizing usernames."""

    def __init__(self, bot):
        self.bot = bot

    def normalized(self, text):
        if text is None:
            return None

        text = unicodedata.normalize("NFKC", text)
        text = re.sub(URL_REGEX, "", text)
        while len(text) > 0 and text[0] < "0":
            text = text[1:]

        if len(text) == 0:
            return None
        return text[:32]

    async def normalize(self, member):
        normalized = self.normalized(member.nick) or self.normalized(member.name) or LAST_RESORT
        if normalized != member.display_name:
            await member.edit(nick=normalized)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.nick != after.nick:
            await self.normalize(after)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.normalize(member)

def setup(bot):
    bot.add_cog(Names(bot))