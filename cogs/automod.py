import asyncio

from nextcord.ext import commands


class Automod(commands.Cog):
    """For automod."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 994266247577485473:
            if member.bot:
                role = member.guild.get_role(994928698593652867)
                await member.add_roles(role)
            else:
                role = member.guild.get_role(994928660157050990)
                await asyncio.sleep(60)
                await member.add_roles(role)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.guild.id == 994266247577485473:
            if before.premium_since is None and after.premium_since is not None:
                self.bot.dispatch("boost_add", after)

            if before.premium_since is not None and after.premium_since is None:
                self.bot.dispatch("boost_remove", after)