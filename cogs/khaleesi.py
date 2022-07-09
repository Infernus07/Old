import asyncio
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
    async def on_message(self, message: nextcord.Message):
        if (
            message.guild is not None and
            message.channel.category is not None and
            message.guild.id == 860180439666917416 and
            message.channel.category.id == 863437651348815872
        ):
            rare_role = message.guild.get_role(900505207023206400)
            sh_role = message.guild.get_role(967501038183645204)

            if rare_role.mention in message.content:
                await self.process(message, 969285850426925117, "🎉｜rare")
                self.redirect(message)

            elif sh_role.mention in message.content:
                await self.process(message, 933538406414319637, "✨｜shiny-hunt")
                self.redirect(message)

            elif (
                message.author.id == 875526899386953779 and
                "Shiny" in message.content and
                len(message.mentions) > 0
            ):
                name = message.content.replace("✨", "").replace("*", "").replace("Pinging", "").replace("Shiny", "").replace("Hunters", "").strip().lower()
                await self.process(message, 933538406414319637, name)

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