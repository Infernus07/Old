from datetime import datetime
import plasma
import random

import nextcord
from nextcord.ext import commands


class Misc(commands.Cog):
    """For miscellaneous commands."""

    def __init__(self, bot):
        self.bot = bot

    def get_acknowledgement(self, ctx, member):
        if member == self.bot.user:
            return f"The Real {self.bot.user.name}"
        if member == ctx.guild.owner:
            return "Server Owner"
        if member.guild_permissions.administrator:
            return "Server Admin"
        if member.premium_since:
            return "Server Booster"
        if member.bot:
            return "Server Bot"
        return None

    def get_permissions(self, member):
        permissions = []
        for i in member.guild_permissions:
            if i[0] in (
                "administrator",
                "manage_guild",
                "manage_roles",
                "manage_channels",
                "manage_messages",
                "manage_webhooks",
                "manage_nicknames",
                "manage_emojis",
                "kick_members",
                "ban_members",
                "moderate_members",
                "mention_everyone"
            ) and i[1]:
                permissions.append(i[0].replace("_", " ").title())
        return permissions

    @plasma.community_server_only()
    @commands.command(aliases=["av"])
    async def avatar(self, ctx, *, member: nextcord.Member = None):
        """Get the avatar of yourself or another user."""

        member = member or ctx.author
        embed = nextcord.Embed(
            color=nextcord.Color.blue(),
            description=f"**[Avatar]({member.display_avatar})**"
        )
        embed.set_author(name=member.display_name, icon_url=member.display_avatar)
        embed.set_image(url=member.display_avatar)

        await ctx.send(embed=embed)

    @plasma.community_server_only()
    @commands.command(aliases=["mc", "members"])
    async def membercount(self, ctx):
        """Get the membercount of the current server."""

        embed = nextcord.Embed(
            color=nextcord.Color.blue(),
            title="Members",
            description=ctx.guild.member_count,
            timestamp=datetime.utcnow()
        )
        await ctx.send(embed=embed)

    @plasma.community_server_only()
    @commands.command(aliases=["si"])
    async def serverinfo(self, ctx):
        """Get information for the current server."""

        embed = nextcord.Embed(
            color=nextcord.Color.blue(),
            timestamp=ctx.guild.created_at
        )
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon)
        embed.set_footer(text=f"ID: {ctx.guild.id} | Server Created")
        embed.set_thumbnail(url=ctx.guild.icon)

        embed.add_field(name="Owner", value=ctx.guild.owner)
        embed.add_field(name="Category Channels", value=len(ctx.guild.categories))
        embed.add_field(name="Text Channels", value=len(ctx.guild.text_channels))
        embed.add_field(name="Voice Channels", value=len(ctx.guild.voice_channels))
        embed.add_field(name="Members", value=ctx.guild.member_count)
        embed.add_field(name="Roles", value=len(ctx.guild.roles))

        await ctx.send(embed=embed)

    @plasma.community_server_only()
    @commands.command()
    async def flip(self, ctx):
        """Flip a coin."""

        await ctx.reply(random.choice(["Tails", "Heads"]))

    @plasma.community_server_only()
    @commands.command()
    async def roll(self, ctx, *, range: plasma.RollConverter = None):
        """Roll a dice."""

        range = range or (1, 100)
        await ctx.send(f"\N{GAME DIE} **{ctx.author.display_name}** rolls **{random.randint(range[0], range[1])}** ({range[0]}-{range[1]})")

    @plasma.community_server_only()
    @commands.command(aliases=["w", "who"])
    async def whois(self, ctx, *, member: nextcord.Member = None):
        """Get information about a user."""

        member = member or ctx.author
        roles = [role.mention for role in member.roles][1:][::-1]
        permissions = self.get_permissions(member)
        acknowledgement = self.get_acknowledgement(ctx, member)

        embed = nextcord.Embed(
            color=nextcord.Color.blue(),
            description=member.mention,
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=member, icon_url=member.display_avatar)
        embed.set_footer(text=f"ID: {member.id}")
        embed.set_thumbnail(url=member.display_avatar)

        embed.add_field(name="Joined", value=member.joined_at.strftime("%a, %b %#d, %Y %I:%M %p"))
        embed.add_field(name="Registered", value=member.created_at.strftime("%a, %b %#d, %Y %I:%M %p"))
        embed.add_field(name=f"Roles [{len(roles)}]", value=" ".join(roles) if len(roles) > 0 else "None", inline=False)

        if permissions:
            embed.add_field(name="Key Permissions", value=", ".join(sorted(permissions)), inline=False)
        if acknowledgement:
            embed.add_field(name="Acknowledgements", value=acknowledgement, inline=False)
            
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Misc(bot))