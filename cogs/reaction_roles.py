from contextlib import suppress

import nextcord
from nextcord.ext import commands

COLOR_MENU = {
    "992838901620297799": 994929905974394880, # Amaranth
    "992838924382785636": 994929940732592148, # Blush
    "992838948021882920": 994929969509711994, # Fuchsia
    "992838970109079583": 994930001822621776, # Ice
    "992838995467845632": 994930024094380052, # Indigo
    "992839028854493317": 994930211604942918, # Lilac
    "992839071510569090": 994930238490419250, # Lime
    "992839096819003512": 994930268274184192, # Midnight
    "992839124459454525": 994930461572874260, # Obsidian
    "992839149495267418": 994930496201035857, # Sky
    "994963175562821666": 994930524160266311, # Snow
    "992839272824570006": 994930553302298684  # Tangerine
}

PING_MENU = {
    "📢": 994929600696164372, # Announcement Ping
    "🍁": 994929659055702056, # Partnership Ping
    "🎁": 994929518823358645, # Event Ping
    "🎉": 994929467564752967, # Giveaway Ping
    "⚡": 994929560032395346, # Incense Ping
    "994953711002583131": 994960313596268705 # Pokemon Raid
}

ACCESS_MENU = {
    "994953622330822797": 994929076735311892, # Poketwo Access
    "994953711002583131": 994929119823405066, # Pokemon Access
    "994953849452380230": 994929146465615892, # Pokecord Access
    "994953905203052564": 994929186726740048, # Deriver Access
    "🤖": 994929186726740048 # Other Bots Access
}


class ReactionRoles(commands.Cog):
    """For reaction roles."""

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.guild_id == 994266247577485473:
            guild = self.bot.get_guild(payload.guild_id)
            user  = guild.get_member(payload.user_id)
            emoji = str(payload.emoji.id) if payload.emoji.is_custom_emoji() else payload.emoji.name

            if payload.message_id == 995008665260134491:
                try:
                    role = guild.get_role(COLOR_MENU[emoji])
                except:
                    message = await guild.get_channel(payload.channel_id).fetch_message(payload.message_id)
                    await message.remove_reaction(payload.emoji, user)
                    return

            elif payload.message_id == 995028284570095656:
                try:
                    role = guild.get_role(PING_MENU[emoji])
                except:
                    message = await guild.get_channel(payload.channel_id).fetch_message(payload.message_id)
                    await message.remove_reaction(payload.emoji, user)
                    return

            elif payload.message_id == 995031116681592832:
                try:
                    role = guild.get_role(ACCESS_MENU[emoji])
                except:
                    message = await guild.get_channel(payload.channel_id).fetch_message(payload.message_id)
                    await message.remove_reaction(payload.emoji, user)
                    return

            if role not in user.roles:
                await user.add_roles(role)

                with suppress(nextcord.Forbidden):
                    message = await user.send(f"Gave you the **{role}** role!")
                    await message.delete(delay=20)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.guild_id == 994266247577485473:
            guild = self.bot.get_guild(payload.guild_id)
            user  = guild.get_member(payload.user_id)
            emoji = str(payload.emoji.id) if payload.emoji.is_custom_emoji() else payload.emoji.name

            if payload.message_id == 995008665260134491:
                role = guild.get_role(COLOR_MENU[emoji])

            elif payload.message_id == 995028284570095656:
                role = guild.get_role(PING_MENU[emoji])

            elif payload.message_id == 995031116681592832:
                role = guild.get_role(ACCESS_MENU[emoji])

            if role in user.roles:
                await user.remove_roles(role)

                with suppress(nextcord.Forbidden):
                    message = await user.send(f"Took away the **{role}** role!")
                    await message.delete(delay=20)

def setup(bot):
    bot.add_cog(ReactionRoles(bot))