from contextlib import suppress
from dataclasses import dataclass
from datetime import datetime
import plasma

import nextcord
from nextcord.ext import commands


@dataclass
class Action:
    target: nextcord.Member
    user: nextcord.Member
    guild: nextcord.Guild
    reason: str = None
    duration: int = None

    async def notify_user(self, ctx):
        embed = nextcord.Embed(
            color=nextcord.Color.green(),
            description=f"{plasma.CHECK} ***{self.target.display_name} was {self.past_tense}.***"
        )
        await ctx.send(embed=embed)

    async def notify_target(self):
        embed = nextcord.Embed(
            color=self.color,
            title=f"{self.emoji} {self.past_tense.title()}",
            description=f"You have been {self.past_tense}",
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Guild", value=self.guild)
        embed.add_field(name="Reason", value=self.reason or "No reason provided.")

        with suppress(nextcord.NotFound):
            await self.target.send(embed=embed)

    async def log(self):
        embed = nextcord.Embed(
            color=self.color,
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=f"{self.type.title()} | {self.target}", icon_url=self.target.display_avatar)
        embed.set_footer(text=f"ID: {self.target.id}")
        embed.add_field(name="User", value=self.target.mention)
        embed.add_field(name="Moderator", value=self.user.mention)
        embed.add_field(name="Reason", value=self.reason or "No reason.")

        channel = self.guild.get_channel(994922728987557918)
        await channel.send(embed=embed)

    def check(self, ctx):
        if ctx.author.top_role <= self.target.top_role:
            raise commands.BadArgument("That user is a mod/admin, I can't do that.")


class Kick(Action):
    type = "kick"
    past_tense = "kicked"
    emoji = "\N{WOMANS BOOTS}"
    color = nextcord.Color.orange()

    async def execute(self, ctx):
        await ctx.message.delete()
        self.check(ctx)
        await ctx.guild.kick(self.target, reason=self.reason or "No reason.")
        await self.notify_user(ctx)
        await self.notify_target()
        await self.log()

class Warn(Action):
    type = "warn"
    past_tense = "warned"
    emoji = "\N{WARNING SIGN}"
    color = nextcord.Color.orange()

    async def execute(self, ctx):
        await ctx.message.delete()
        self.check(ctx)
        await self.notify_user(ctx)
        await self.notify_target()
        await self.log()

class Mute(Action):
    type = "mute"
    past_tense = "muted"
    emoji = "\N{SPEAKER WITH CANCELLATION STROKE}"
    color = nextcord.Color.orange()

    async def execute(self, ctx):
        await ctx.message.delete()
        self.check(ctx)
        await self.target.timeout(self.duration, reason=self.reason or "No reason.")
        await self.notify_user(ctx)
        await self.notify_target()
        await self.log()

class Unmute(Action):
    type = "unmute"
    past_tense = "unmuted"
    emoji = "\N{SPEAKER}"
    color = nextcord.Color.green()

    async def execute(self, ctx):
        await ctx.message.delete()
        await self.target.timeout(None, reason=self.reason or "No reason")
        await self.notify_user(ctx)
        await self.notify_target()
        await self.log()

class Ban(Action):
    type = "ban"
    past_tense = "banned"
    emoji = "\N{HAMMER}"
    color = nextcord.Color.red()

    async def execute(self, ctx):
        await ctx.message.delete()
        self.check(ctx)
        await self.notify_target()
        await ctx.guild.ban(self.target, reason=self.reason or "No reason.")
        await self.notify_user(ctx)
        await self.log()

class Unban(Action):
    type = "unban"
    past_tense = "unbanned"
    emoji = "\N{OPEN LOCK}"
    color = nextcord.Color.green()

    async def execute(self, ctx):
        await ctx.message.delete()
        await ctx.guild.unban(self.target, reason=self.reason or "No reason.")
        await self.notify_user(ctx)
        await self.log()


class Moderation(commands.Cog):
    """For moderation"""

    def __init__(self, bot):
        self.bot = bot

    @commands.check_any(commands.is_owner(), plasma.is_trial_moderator())
    @commands.command()
    async def purge(self, ctx, count: int):
        """Delete a number of messages from a channel."""

        await ctx.message.delete()
        await ctx.channel.purge(limit=count, check=lambda m: not m.pinned)

    @commands.check_any(commands.is_owner(), plasma.is_manager())
    @commands.command()
    async def kick(self, ctx, member: nextcord.Member, *, reason=None):
        """Kick a member."""

        action = Kick(
            target=member,
            user=ctx.author,
            guild=ctx.guild,
            reason=reason
        )
        await action.execute(ctx)

    @commands.check_any(commands.is_owner(), plasma.is_moderator())
    @commands.command()
    async def mute(self, ctx, member: nextcord.Member, duration, *, reason=None):
        """Mute a member."""

        if member.communication_disabled_until is not None:
            raise commands.BadArgument(f"{member.display_name} is already muted.")

        action = Mute(
            target=member,
            user=ctx.author,
            guild=ctx.guild,
            reason=reason,
            duration=duration
        )
        await action.execute(ctx)

    @commands.check_any(commands.is_owner(), plasma.is_moderator())
    @commands.command()
    async def unmute(self, ctx, member: nextcord.Member, *, reason=None):
        """Unmute a member."""

        if member.communication_disabled_until is None:
            raise commands.BadArgument(f"{member.display_name} is not muted.")

        action = Unmute(
            target=member,
            user=ctx.author,
            guild=ctx.guild,
            reason=reason
        )
        await action.execute(ctx)

    @commands.check_any(commands.is_owner(), plasma.is_manager())
    @commands.command()
    async def ban(self, ctx, member: nextcord.Member, *, reason=None):
        """Ban a member."""

        bans = await ctx.guild.bans()
        member_name, member_discriminator = str(member).split("#")

        if bans:
            for entry in bans:
                user = entry.user
                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    raise commands.BadArgument(f"{user} is already banned.")

        action = Ban(
            target=member,
            user=ctx.author,
            guild=ctx.guild,
            reason=reason
        )
        await action.execute(ctx)

    @commands.check_any(commands.is_owner(), plasma.is_manager())
    @commands.command()
    async def unban(self, ctx, member: nextcord.User, *, reason=None):
        """Unban a member."""

        bans = await ctx.guild.bans()
        member_name, member_discriminator = str(member).split("#")
        check = None

        action = Unban(
            target=member,
            user=ctx.author,
            guild=ctx.guild,
            reason=reason
        )

        if bans:
            for entry in bans:
                user = entry.user
                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    action.target = user
                    await action.execute(ctx)
                    check = True
                    break

            if not check:
                raise commands.BadArgument(f"{member} was not banned.")
        raise commands.BadArgument(f"{member} was not banned.")

def setup(bot):
    bot.add_cog(Moderation(bot))