import asyncio
from contextlib import suppress
from datetime import timedelta
import plasma
import re

import nextcord
from nextcord.ext import commands


class Automod(commands.Cog):
    """For automod."""

    def __init__(self, bot):
        self.bot = bot
        self.cooldown = commands.CooldownMapping.from_cooldown(15, 17, commands.BucketType.member)
        self.invite_regex = re.compile(r"(?:https?://)?discord(?:app)?\.(?:com/invite|gg)/([a-zA-Z0-9]+)/?", flags=re.I)

    async def notify(self, message, text):
        with suppress(nextcord.NotFound):
            await message.delete()
        await message.channel.send(f"{message.author.mention} {text}", delete_after=5)

    @commands.Cog.listener(name="on_message")
    @commands.Cog.listener(name="on_message_edit")
    async def on_message(self, *args):
        message = args[-1]

        if (
            message.guild is None
            or message.guild.id != 994266247577485473
            or not isinstance(message.author, nextcord.Member)
            or message.author.bot
            or message.author.guild_permissions.administrator
            or message.author.id in plasma.OWNERS
        ):
            return

        words = message.content.lower().split(" ")
        for i in plasma.BANNED_WORDS:
            if any(i in x for x in words):
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
                await message.channel.purge(limit=15, check=lambda m: m.author == message.author)
                await message.channel.send(f"{message.author.mention} No spamming!", delete_after=5)
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

def setup(bot):
    bot.add_cog(Automod(bot))