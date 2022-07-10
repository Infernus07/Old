from contextlib import suppress
import plasma

import nextcord
from nextcord.ext import commands


PING_MENU = {
    "📢": 994929600696164372, # Announcement Ping
    "🍁": 994929659055702056, # Partnership Ping
    "🎁": 994929518823358645, # Event Ping
    "🎉": 994929467564752967, # Giveaway Ping
    "⚡": 994929560032395346, # Incense Ping
    f"{plasma.Emoji.pokemon().id}": 994960313596268705 # Pokemon Raid
}

ACCESS_MENU = {
    f"{plasma.Emoji.poketwo().id}" : 994929076735311892, # Poketwo Access
    f"{plasma.Emoji.pokemon().id}" : 994929119823405066, # Pokemon Access
    f"{plasma.Emoji.pokecord().id}": 994929146465615892, # Pokecord Access
    f"{plasma.Emoji.deriver().id}" : 994929186726740048, # Deriver Access
    "🤖": 994929219568156702 # Other Bots Access
}

RARE_MENU = {
    f"{plasma.Emoji.pokemon().id}" : 994960527287668826, # Pokemon Rares
    f"{plasma.Emoji.pokecord().id}": 994960678366494782, # Pokecord Rares
    f"{plasma.Emoji.deriver().id}" : 994960742103142420  # Deriver Rares
}


class ReactionRoles(commands.Cog):
    """For reaction roles."""

    def __init__(self, bot):
        self.bot = bot

    async def remove_reaction(self, payload, guild, user):
        message = await guild.get_channel(payload.channel_id).fetch_message(payload.message_id)
        await message.remove_reaction(payload.emoji, user)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id != self.bot.user.id:
            guild = self.bot.get_guild(payload.guild_id)
            user  = guild.get_member(payload.user_id)
            emoji = str(payload.emoji.id) if payload.emoji.is_custom_emoji() else payload.emoji.name
            role = None

            if payload.message_id == 995701370785108130:
                try:
                    role = guild.get_role(PING_MENU[emoji])
                except:
                    await self.remove_reaction(payload, guild, user)
                    return

            elif payload.message_id == 995704076719370240:
                try:
                    role = guild.get_role(ACCESS_MENU[emoji])
                except:
                    await self.remove_reaction(payload, guild, user)
                    return

            elif payload.message_id == 995667586060652604:
                if (
                    guild.premium_subscriber_role not in user.roles
                    and user.id not in plasma.OWNERS
                    and not any(x.id in [994927712135286828, 994927785351053362, 995608606609252406] for x in user.roles)
                ):
                    await self.remove_reaction(payload, guild, user)
                    with suppress(nextcord.Forbidden):
                        await user.send("You must be a server booster to get the rares role.")
                        return
                try:
                    role = guild.get_role(RARE_MENU[emoji])
                except:
                    await self.remove_reaction(payload, guild, user)
                    return

            if role is not None and role not in user.roles:
                await user.add_roles(role)
                with suppress(nextcord.Forbidden):
                    await user.send(f"Gave you the **{role}** role!")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.user_id != self.bot.user.id:
            guild = self.bot.get_guild(payload.guild_id)
            user  = guild.get_member(payload.user_id)
            emoji = str(payload.emoji.id) if payload.emoji.is_custom_emoji() else payload.emoji.name
            role = None

            if payload.message_id == 995701370785108130:
                with suppress(KeyError):
                    role = guild.get_role(PING_MENU[emoji])

            elif payload.message_id == 995704076719370240:
                with suppress(KeyError):
                    role = guild.get_role(ACCESS_MENU[emoji])

            elif payload.message_id == 995667586060652604:
                with suppress(KeyError):
                    role = guild.get_role(RARE_MENU[emoji])

            if role is not None and role in user.roles:
                await user.remove_roles(role)
                with suppress(nextcord.Forbidden):
                    await user.send(f"Took away the **{role}** role!")

def setup(bot):
    bot.add_cog(ReactionRoles(bot))