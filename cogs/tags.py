import plasma

import nextcord
from nextcord.ext import commands


class Tags(commands.Cog):
    """For tags."""

    def __init__(self, bot):
        self.bot = bot
        self.col = plasma.mongo.tag

    def has_profanity(self, *, content=None, name=None):
        if content:
            words = content.split()
            for i in plasma.BANNED_WORDS:
                if any(i in x for x in words):
                    return True

        if name:
            words = name.split()
            for i in plasma.BANNED_WORDS:
                if any(i in x for x in words):
                    return True

        return False

    def find(self, name):
        doc = self.col.find_one({"alias": name.lower()})
        if doc is None:
            raise commands.BadArgument(f"Could not find a tag matching `{name}`.")
        return doc

    async def send(self, ctx, message):
        embed = nextcord.Embed(
            color=nextcord.Color.green(),
            description=f"{plasma.Emoji.check()} {message}"
        )
        await ctx.send(embed=embed)

    @commands.check_any(plasma.community_server_only(), plasma.test_server_only())
    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def tag(self, ctx, *, name):
        """Get a tag."""

        name = name.strip()
        doc = self.find(name)

        await ctx.send(doc["content"], allowed_mentions=nextcord.AllowedMentions.none())
        self.col.update_one({"alias": name.lower()}, {"$inc": {"uses": 1}})

    @commands.check_any(plasma.community_server_only(), plasma.test_server_only())
    @tag.command()
    async def create(self, ctx, name, *, content):
        """Creates a new tag owned by you."""

        content = content.strip()
        if self.has_profanity(content=content, name=name):
            return

        doc = self.col.find_one({"alias": name.lower()})
        if doc is not None:
            raise commands.BadArgument(f"A tag with the name `{name}` already exists.")

        doc = {
            "_id": name.lower(),
            "alias": [name.lower()],
            "content": content,
            "owner_id": ctx.author.id,
            "uses": 0
        }
        self.col.insert_one(doc)
        await self.send(ctx, f"Tag {name} created.")

    @commands.check_any(plasma.community_server_only(), plasma.test_server_only())
    @tag.command()
    async def delete(self, ctx, *, name):
        """Removes a tag that you own."""

        name = name.strip()
        doc = self.find(name)

        if doc["owner_id"] != ctx.author.id and doc["owner_id"] not in plasma.OWNERS:
            raise commands.BadArgument("You do not own that tag.")

        confirm = await plasma.get_confirmation(ctx, f"Are you sure you want to delete `{name}`?")
        if confirm:
            self.col.delete_one({"alias": name.lower()})
            await self.send(ctx, f"Tag {name} deleted.")

    @commands.check_any(plasma.community_server_only(), plasma.test_server_only())
    @tag.command()
    async def edit(self, ctx, name, *, content):
        """Modifies an existing tag that you own."""

        content = content.strip()
        doc = self.find(name)

        if self.has_profanity(content=content):
            return

        if doc["owner_id"] != ctx.author.id and doc["owner_id"] not in plasma.OWNERS:
            raise commands.BadArgument("You do not own that tag.")

        self.col.update_one({"alias": name.lower()}, {"$set": {"content": content}})
        await self.send(ctx, f"Tag {name} edited.")

    @commands.check_any(plasma.community_server_only(), plasma.test_server_only())
    @tag.command()
    async def info(self, ctx, *, name):
        """Retrieves info about a tag."""

        name = name.strip()
        doc = self.find(name)
        user = self.bot.get_user(doc["owner_id"])
        if user is None:
            user = plasma.FakeUser(doc["owner_id"])

        embed = nextcord.Embed(
            color=nextcord.Color.blue(),
            title=plasma.title(doc["_id"])
        )
        embed.set_author(name=user, icon_url=user.display_avatar)
        embed.add_field(name="Owner", value=user.mention)
        if len(doc["alias"]) > 1:
            alias = doc["alias"]
            alias.pop(0)
            embed.add_field(name="Aliases", value=", ".join(alias))
        embed.add_field(name="Uses", value=doc["uses"])

        await ctx.send(embed=embed)

    @commands.check_any(plasma.community_server_only(), plasma.test_server_only())
    @tag.command()
    async def transfer(self, ctx, member: nextcord.Member, *, name):
        """Transfers a tag that you own to another user."""

        name = name.strip()
        doc = self.find(name)

        if doc["owner_id"] != ctx.author.id and doc["owner_id"] not in plasma.OWNERS:
            raise commands.BadArgument("You do not own that tag.")

        if doc["owner_id"] == member.id:
            raise commands.BadArgument(f"{member.display_name} already owns that tag.")

        self.col.update_one({"alias": name.lower()}, {"$set": {"owner_id": member.id}})
        await self.send(ctx, f"Successfully transferred tag to {member.display_name}.")

    @plasma.community_server_only()
    @tag.command()
    async def claim(self, ctx, *, name):
        """Claims a tag whose owner is no longer in the server."""

        name = name.strip()
        doc = self.find(name)
        member = ctx.guild.get_member(doc["owner_id"])

        if member is not None:
            raise commands.BadArgument("Tag owner is still in the server.")

        self.col.update_one({"alias": name.lower()}, {"$set": {"owner_id": ctx.author.id}})
        await self.send(ctx, f"Successfully claimed `{name}`.")

    @commands.check_any(plasma.community_server_only(), plasma.test_server_only())
    @tag.command()
    async def clear(self, ctx):
        """Removes all tags that you own."""

        doc = list(self.col.find({"owner": ctx.author.id}).sort("uses", -1))
        if len(doc) == 0:
            raise commands.BadArgument("You don't have any tags.")

        confirm = await plasma.get_confirmation(ctx, "Are you sure you want to delete **all** of your tags?")
        if confirm:
            self.col.delete_many({"owner_id": ctx.author.id})
            await self.send(ctx, "Deleted all of your tags.")

    @commands.check_any(plasma.community_server_only(), plasma.test_server_only())
    @tag.command()
    async def alias(self, ctx, name, *, alias):
        """Creates an alias for a pre-existing tag."""

        alias = alias.strip()
        self.find(name)

        doc = self.col.find_one({"alias": alias.lower()})
        if doc is not None:
            raise commands.BadArgument(f"A tag with the name `{alias}` already exists.")

        self.col.update_one({"alias": name.lower()}, {"$push": {"alias": alias.lower()}})
        await self.send(ctx, f"Successfully created an alias `{alias}` for `{name}`.")

def setup(bot):
    bot.add_cog(Tags(bot))