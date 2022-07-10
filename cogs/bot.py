from datetime import datetime
import plasma

import nextcord
from nextcord.ext import commands


class Bot(commands.Cog):
    """For basic bot operation."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, (plasma.CommandError, commands.CommandNotFound, commands.CheckAnyFailure)):
            return

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.message.add_reaction("\N{HOURGLASS}")
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send_help(ctx.command)
            return

        if isinstance(error, (commands.BadArgument, commands.CheckFailure, commands.UserInputError)):
            embed = nextcord.Embed(
                color=nextcord.Color.red(),
                description=f"{plasma.Emoji.cross()} {error}"
            )
            await ctx.send(embed=embed)
            return

    @commands.Cog.listener()
    async def on_error(self, *args, **kwargs):
        return

    @commands.Cog.listener()
    async def on_application_command_error(self, interaction, error):
        embed = nextcord.Embed(
            color=nextcord.Color.red(),
            description=f"{plasma.Emoji.cross()} {error}"
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content != after.content:
            await self.bot.process_commands(after)

    
    @plasma.community_server_only()
    @commands.command()
    async def ping(self, ctx):
        """View the bot's latency."""

        message = await ctx.send("Pong!")
        ms = int((message.created_at - ctx.message.created_at).total_seconds() * 1000)
        await message.edit(content=f"Pong! **{ms} ms**")

    @plasma.community_server_only()
    @commands.cooldown(3, 8, commands.BucketType.user)
    @commands.command()
    async def report(self, ctx, member: nextcord.Member, *, reason=None):
        """"Reports a member to the server's staff."""

        if member.bot or member == ctx.author:
            raise commands.BadArgument("You cannot report {}.".format("bots" if member.bot else "yourself"))

        embed = nextcord.Embed(
            color=nextcord.Color.green(),
            description=f"{plasma.Emoji.check()} User reported to the proper authorities."
        )
        await ctx.send(embed=embed)

        embed = nextcord.Embed(
            color=nextcord.Color.blue(),
            description=f"**[Jump to message]({ctx.message.jump_url})**",
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=f"Report | {member}", icon_url=member.display_avatar)
        embed.add_field(name="Member", value=member.mention)
        embed.add_field(name="User", value=ctx.author.mention)
        embed.add_field(name="Reason", value=reason.strip() if reason else "No reason.")

        channel = self.bot.get_channel(995334142285848727)
        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Bot(bot))