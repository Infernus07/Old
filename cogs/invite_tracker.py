from nextcord.ext import commands


class InviteTracker(commands.Cog):
    """For invite tracker."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.id == 994266247577485473:
            channel = self.bot.get_channel(994922728987557918)
            await channel.send(f"{member.mention} just left the server.")

def setup(bot):
    bot.add_cog(InviteTracker(bot))