from nextcord.ext import commands


class Reactions(commands.Cog):
    """For reacting."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in (994920672574832742, 995244940340772864):
            await message.add_reaction("<a:_:995243875906097252>")

def setup(bot):
    bot.add_cog(Reactions(bot))