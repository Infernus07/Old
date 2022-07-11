import asyncio
from contextlib import suppress
from datetime import timedelta
import plasma
import re
import unicodedata

import nextcord
from nextcord.ext import commands


class Automod(commands.Cog):
    """For automod."""

    def __init__(self, bot):
        self.bot = bot
        self.cooldown = commands.CooldownMapping.from_cooldown(15, 17, commands.BucketType.member)
        self.invite_regex = re.compile(plasma.INVITE_REGEX, flags=re.I)
        self.url_regex = re.compile(plasma.URL_REGEX)

    def normalized(self, text):
        if text is None:
            return None

        text = unicodedata.normalize("NFKC", text)
        text = re.sub(self.url_regex, "", text)
        while len(text) > 0 and text[0] < "0":
            text = text[1:]

        if len(text) == 0:
            return None
        return text[:32]

    async def normalize(self, member):
        normalized = self.normalized(member.nick) or self.normalized(member.name) or "User"
        if normalized != member.display_name:
            await member.edit(nick=normalized)

    async def notify(self, message, text, *, purge=False):
        if purge:
            await message.channel.purge(limit=15, check=lambda m: m.author == message.author)
        else:
            with suppress(nextcord.NotFound):
                await message.delete()
        await message.channel.send(f"{message.author.mention} {text}", delete_after=5)

    @commands.Cog.listener(name="on_message")
    @commands.Cog.listener(name="on_message_edit")
    async def on_message(self, *args):
        message = args[-1]

        if message.channel.id in (994920672574832742, 995244940340772864):
            await message.add_reaction(plasma.Emoji.red_tick())

        if (
            message.guild is None
            or message.guild.id != 994266247577485473
            or not isinstance(message.author, nextcord.Member)
            or message.author.bot
            or message.author.guild_permissions.administrator
            or message.author.id in plasma.OWNERS
        ):
            return

        words = plasma.profanity_words(message.content)
        if any(x in words for x in plasma.BANNED_WORDS):
            await self.notify(message, "Watch your language!")
            return

        for code in self.invite_regex.findall(message.content):
            with suppress(nextcord.NotFound):
                invite = await self.bot.fetch_invite(code)
                if invite.guild != message.guild:
                    await self.notify(message, "No invite links!")
                    await message.author.timeout(nextcord.utils.utcnow() + timedelta(minutes=10))
                    return

        if len(message.mentions) >= 10:
            await self.notify(message, "No mass mentions!")
            return

        if message.channel.id != 994921223500877909:
            bucket = self.cooldown.get_bucket(message)
            if bucket.update_rate_limit():
                self.cooldown._cache[self.cooldown._bucket_key(message)].reset()
                await self.notify(message, "No spamming!", purge=True)
                return

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id != 994266247577485473:
            return

        if member.bot:
            role = member.guild.get_role(994928698593652867)
            await member.add_roles(role)

        else:
            role = member.guild.get_role(994928660157050990)
            await asyncio.sleep(60)
            await member.add_roles(role)

        await self.normalize(member)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.id != 994266247577485473:
            return

        channel = self.bot.get_channel(994922728987557918)
        await channel.send(f"{member.mention} just left the server.")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.nick != after.nick:
            await self.normalize(after)

def setup(bot):
    bot.add_cog(Automod(bot))