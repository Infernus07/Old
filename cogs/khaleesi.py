import asyncio
import plasma
import requests

import nextcord
from nextcord.ext import commands


class Khaleesi(commands.Cog):
    """For khaleesi."""

    def __init__(self, bot):
        self.bot = bot

    def redirect(self, message):
        category = nextcord.utils.get(message.guild.categories, id=863437651348815872)
        channels = ""

        for i in category.channels:
            if i != message.channel:
                channels += f"<#{i.id}> "
        requests.post("https://discord.com/api/v9/channels/967466145965834310/messages", {"content": f"<@716390085896962058> redirect {channels}"}, headers={"authorization": "OTY3NDQwMjY3MDc2NTcxMTg2.YmUY_g.p_gS9Wdv8KrziY30PZz4AW4Rpoc"})

    async def process(self, message, category_id, name):
        channel = await message.channel.clone(name=message.channel.name)
        await channel.edit(position=message.channel.position)

        category = nextcord.utils.get(message.guild.categories, id=category_id)
        await message.channel.edit(name=name, category=category)

    @commands.Cog.listener()
    async def on_message(self, message):
        if (
            message.guild is None
            or message.guild.id != 860180439666917416
            or message.channel.category is None
            or message.channel.category.id != 863437651348815872
        ):
            return

        rare_role = message.guild.get_role(900505207023206400)
        sh_role = message.guild.get_role(967501038183645204)

        if rare_role.mention in message.content:
            await self.process(message, 969285850426925117, "🎉｜rare")
            self.redirect(message)
            return

        if sh_role.mention in message.content:
            await self.process(message, 933538406414319637, "✨｜shiny-hunt")
            self.redirect(message)
            return

        if (
            message.author.id == 875526899386953779
            and "Shiny" in message.content
            and len(message.mentions) > 0
        ):
            name = plasma.sub(message.content, ("✨", "*", "Pinging", "Shiny", "Hunters")).lower()
            await self.process(message, 933538406414319637, name)
            return

    @nextcord.slash_command(guild_ids=[860180439666917416], description="Deletes the current channel.")
    async def close(self, interaction):
        embed = nextcord.Embed(
            color=nextcord.Color.red(),
            description="This channel will be deleted in a few seconds."
        )
        await interaction.response.send_message(embed=embed)
        await asyncio.sleep(5)
        await interaction.channel.delete()

def setup(bot):
    bot.add_cog(Khaleesi(bot))