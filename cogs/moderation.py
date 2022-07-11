from contextlib import suppress
from dataclasses import dataclass
from datetime import datetime
import plasma

import nextcord
from nextcord.ext import commands


@dataclass
class Action:
    context: commands.Context
    target: nextcord.Member
    reason: str = None
    duration: datetime = None

    async def notify_user(self):
        embed = nextcord.Embed(
            color=nextcord.Color.green(),
            description=f"{plasma.Emoji.check()} ***{self.target.display_name} was {self.past_tense}.***"
        )
        await self.context.send(embed=embed)

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


class Kick(Action):
    type = "kick"
    past_tense = "kicked"
    emoji = "\N{WOMANS BOOTS}"
    color = nextcord.Color.orange()

    async def execute(self):
        await self.notify_target()
        await self.context.guild.kick(self.target, reason=self.reason or "No reason.")
        await self.notify_user()
        await self.log()


class Warn(Action):
    type = "warn"
    past_tense = "warned"
    emoji = "\N{WARNING SIGN}"
    color = nextcord.Color.orange()

    async def execute(self):
        plasma.mongo.update_member(self.target, {"$inc": {"warns": 1}})
        await self.notify_user()
        await self.notify_target()
        await self.log()

    async def remove(self, n):
        doc = plasma.mongo.find_member(self.target)
        count = 0 if doc["warns"] - n <= 0 else doc["warns"] - n

        if doc["warns"] == 0:
            raise commands.BadArgument(f"{self.target.display_name} does not have any warns.")

        plasma.mongo.update_member(self.target, {"$set": {"warns": count}})
        embed = nextcord.Embed(
            color=nextcord.Color.green(),
            description=f"{plasma.Emoji.check()} ***Removed {n} warnings from {self.target.display_name}.***"
        )
        await self.context.send(embed=embed)


class Mute(Action):
    type = "mute"
    past_tense = "muted"
    emoji = "\N{SPEAKER WITH CANCELLATION STROKE}"
    color = nextcord.Color.orange()

    async def execute(self):
        await self.target.timeout(self.duration, reason=self.reason or "No reason.")
        await self.notify_user()
        await self.notify_target()
        await self.log()


class Unmute(Action):
    type = "unmute"
    past_tense = "unmuted"
    emoji = "\N{SPEAKER}"
    color = nextcord.Color.green()

    async def execute(self):
        await self.target.timeout(None, reason=self.reason or "No reason.")
        await self.notify_user()
        await self.notify_target()
        await self.log()


class Ban(Action):
    type = "ban"
    past_tense = "banned"
    emoji = "\N{HAMMER}"
    color = nextcord.Color.red()

    async def execute(self):
        await self.notify_target()
        await self.context.guild.ban(self.target, reason=self.reason or "No reason")
        await self.notify_user()
        await self.log()


class Unban(Action):
    type = "unban"
    past_tense = "unbanned"
    emoji = "\N{OPEN LOCK}"
    color = nextcord.Color.green()

    async def execute(self):
        await self.context.guild.unban(self.target, reason=self.reason or "No reason")
        await self.notify_user()
        await self.log()


class Moderation(commands.Cog):
    """For moderation"""

    def __init__(self, bot):
        self.bot = bot

    @plasma.community_server_only()
    @commands.check_any(commands.is_owner(), plasma.is_trial_moderator())
    @commands.cooldown(3, 8, commands.BucketType.user)
    @commands.command()
    async def purge(self, ctx, count: int):
        """Delete a number of messages from a channel."""

        await ctx.channel.purge(limit=count + 1, check=lambda m: not m.pinned)

    @plasma.community_server_only()
    @commands.check_any(commands.is_owner(), plasma.is_manager())
    @commands.cooldown(3, 8, commands.BucketType.user)
    @commands.command()
    async def kick(self, ctx, member: nextcord.Member, *, reason=None):
        """Kick a member."""

        await ctx.message.delete()

        if ctx.author.top_role <= self.target.top_role:
            raise commands.BadArgument("That user is a mod/admin, I can't do that.")

        action = Kick(ctx, member, reason)
        await action.execute()

    @plasma.community_server_only()
    @commands.check_any(commands.is_owner(), plasma.is_trial_moderator())
    @commands.cooldown(3, 8, commands.BucketType.user)
    @commands.command()
    async def warn(self, ctx, member: nextcord.Member, *, reason=None):
        """Warn a member."""

        await ctx.message.delete()

        if ctx.author.top_role <= self.target.top_role:
            raise commands.BadArgument("That user is a mod/admin, I can't do that.")

        action = Warn(ctx, member, reason)
        await action.execute()

    @plasma.community_server_only()
    @commands.check_any(commands.is_owner(), plasma.is_trial_moderator())
    @commands.cooldown(3, 8, commands.BucketType.user)
    @commands.command(aliases=["rwarn"])
    async def removewarn(self, ctx, *, member: nextcord.Member):
        """Remove warn."""

        await ctx.message.delete()

        if ctx.author == member:
            raise commands.BadArgument("You cannot remove your warns.")

        action = Warn(ctx, member)
        await action.remove(1)

    @plasma.community_server_only()
    @commands.check_any(commands.is_owner(), plasma.is_trial_moderator())
    @commands.cooldown(3, 8, commands.BucketType.user)
    @commands.command()
    async def warnings(self, ctx, *, member: nextcord.Member = None):
        """Shows warnings of a member."""

        member = member or ctx.author
        doc = plasma.mongo.find_member(member)

        embed = nextcord.Embed(
            color=nextcord.Color.blue(),
            title=f"Warnings: {member.display_name}",
            description=doc["warns"],
            timestamp=datetime.utcnow()
        )
        embed.set_thumbnail(url=member.display_avatar)
        await ctx.send(embed=embed)

    @plasma.community_server_only()
    @commands.is_owner()
    @commands.command(aliases=["cwarn"])
    async def clearwarn(self, ctx, member: nextcord.Member, *, count: int = 1):
        """Clear warn."""

        await ctx.message.delete()
        
        action = Warn(ctx, member)
        await action.remove(count)

    @plasma.community_server_only()
    @commands.check_any(commands.is_owner(), plasma.is_moderator())
    @commands.cooldown(3, 8, commands.BucketType.user)
    @commands.command()
    async def mute(self, ctx, member: nextcord.Member, duration: plasma.TimeConverter, *, reason=None):
        """Mute a member."""

        await ctx.message.delete()

        if member.communication_disabled_until is not None:
            raise commands.BadArgument(f"{member.display_name} is already muted.")

        if ctx.author.top_role <= self.target.top_role:
            raise commands.BadArgument("That user is a mod/admin, I can't do that.")

        action = Mute(ctx, member, reason, duration)
        await action.execute()

    @plasma.community_server_only()
    @commands.check_any(commands.is_owner(), plasma.is_moderator())
    @commands.cooldown(3, 8, commands.BucketType.user)
    @commands.command()
    async def unmute(self, ctx, member: nextcord.Member, *, reason=None):
        """Unmute a member."""

        await ctx.message.delete()

        if member.communication_disabled_until is None:
            raise commands.BadArgument(f"{member.display_name} is not muted.")

        action = Mute(ctx, member, reason)
        await action.execute()

    @plasma.community_server_only()
    @commands.check_any(commands.is_owner(), plasma.is_manager())
    @commands.cooldown(3, 8, commands.BucketType.user)
    @commands.command()
    async def ban(self, ctx, member: nextcord.Member, *, reason=None):
        """Ban a member."""

        await ctx.message.delete()

        if ctx.author.top_role <= self.target.top_role:
            raise commands.BadArgument("That user is a mod/admin, I can't do that.")

        bans = await ctx.guild.bans()
        member_name, member_discriminator = str(member).split("#")

        if bans:
            for entry in bans:
                user = entry.user
                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    raise commands.BadArgument(f"{user} is already banned.")

        action = Ban(ctx, member, reason)
        await action.execute()

    @plasma.community_server_only()
    @commands.check_any(commands.is_owner(), plasma.is_manager())
    @commands.cooldown(3, 8, commands.BucketType.user)
    @commands.command()
    async def unban(self, ctx, member: nextcord.User, *, reason=None):
        """Unban a member."""

        action = Unban(ctx, member, reason)
        bans = await ctx.guild.bans()
        member_name, member_discriminator = str(member).split("#")
        check = None

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