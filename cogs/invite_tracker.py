from nextcord.ext import commands

LOG_CHANNEL = 994922728987557918


class InviteTracker(commands.Cog):
    """For invite tracker."""

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.bot.get_channel(LOG_CHANNEL).send(f"{member} just left the server.")

def setup(bot):
    bot.add_cog(InviteTracker(bot))