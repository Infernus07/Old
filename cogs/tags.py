import plasma

import nextcord
from nextcord.ext import commands


class Tags(commands.Cog):
    """For tags."""

    def __init__(self, bot):
        self.bot = bot
        self.col = plasma.mongo.tag

    def page_source(self, entries, *, title, icon_url, per_page=20):
        total = len(entries) // per_page
        pages = []
        front, rear = 0, 0

        for i in range(total):
            embed = nextcord.Embed(color=nextcord.Color.blue(), description="")
            front = rear
            rear += per_page

            for j in range(front, rear):
                embed.description += f"{j+1}. {entries[j]['_id']}\n"
            embed.set_author(name=title, icon_url=icon_url)
            embed.set_footer(text=f"Showing {front+1}-{rear} out of {len(entries)}.")
            pages.append(embed)

        embed = nextcord.Embed(color=nextcord.Color.blue(), description="")
        for i in range(rear, len(entries)):
            embed.description += f"{i+1}. {entries[i]['_id']}\n"
        embed.set_author(name=title, icon_url=icon_url)
        embed.set_footer(text=f"Showing {rear+1}-{len(entries)} out of {len(entries)}.")
        pages.append(embed)

        return pages

    def has_profanity(self, *, content=None, name=None):
        if content:
            words = plasma.profanity_words(content)
            if any(x in words for x in plasma.BANNED_WORDS):
                return True

        if name:
            words = plasma.profanity_words(name)
            if any(x in words for x in plasma.BANNED_WORDS):
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

    @plasma.community_and_test_server_only()
    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def tag(self, ctx, *, name):
        """Get a tag."""

        name = name.strip()
        doc = self.find(name)

        await ctx.send(doc["content"], allowed_mentions=nextcord.AllowedMentions.none())
        self.col.update_one({"alias": name.lower()}, {"$inc": {"uses": 1}})

    @plasma.community_and_test_server_only()
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
        await self.send(ctx, f"Tag `{name}` created.")

    @plasma.community_and_test_server_only()
    @commands.is_owner()
    @tag.command()
    async def bot(self, ctx, name, *, content):
        """Creates a new tag owned by the bot."""

        content = content.strip()
        if self.has_profanity(content=content, name=name):
            raise commands.BadArgument("Tags cannot have profanity.")

        doc = self.col.find_one({"alias": name.lower()})
        if doc is not None:
            raise commands.BadArgument(f"A tag with the name `{name}` already exists.")

        doc = {
            "_id": name.lower(),
            "alias": [name.lower()],
            "content": content,
            "owner_id": self.bot.user.id,
            "uses": 0
        }
        self.col.insert_one(doc)
        await self.send(ctx, f"Tag `{name}` created.")

    @plasma.community_and_test_server_only()
    @tag.command()
    async def delete(self, ctx, *, name):
        """Removes a tag that you own."""

        name = name.strip()
        doc = self.find(name)

        if ctx.author.id != doc["owner_id"] and ctx.author.id not in plasma.OWNERS:
            raise commands.BadArgument("You do not own that tag.")

        confirm = await plasma.get_confirmation(ctx, f"Are you sure you want to delete `{name}`?")
        if confirm:
            self.col.delete_one({"alias": name.lower()})
            await self.send(ctx, f"Tag `{name}` deleted.")

    @plasma.community_and_test_server_only()
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
        await self.send(ctx, f"Tag `{name}` edited.")

    @plasma.community_and_test_server_only()
    @tag.command()
    async def search(self, ctx, *, text):
        """Searches for a tag."""

        doc = list(self.col.find({"$text": {"$search": text}}))
        if len(doc) == 0:
            raise commands.BadArgument("No tags found.")

        pages = self.page_source(doc, title="Tags", icon_url=self.bot.user.avatar)
        view = plasma.Pagination(ctx, pages)
        view.message = await ctx.send(embed=pages[0], view=view)

    @plasma.community_and_test_server_only()
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

    @plasma.community_and_test_server_only()
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

    @plasma.community_and_test_server_only()
    @tag.command()
    async def clear(self, ctx):
        """Removes all tags that you own."""

        doc = list(self.col.find({"owner_id": ctx.author.id}).sort("uses", -1))
        if len(doc) == 0:
            raise commands.BadArgument("You don't have any tags.")

        confirm = await plasma.get_confirmation(ctx, "Are you sure you want to delete **all** of your tags?")
        if confirm:
            self.col.delete_many({"owner_id": ctx.author.id})
            await self.send(ctx, "Deleted all of your tags.")

    @plasma.community_and_test_server_only()
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

    @plasma.community_and_test_server_only()
    @commands.command()
    async def tags(self, ctx, *, member: nextcord.Member = None):
        """Lists all tags."""

        if member is None:
            doc = list(self.col.find().sort("uses", -1))
            title = "Tags"
            icon_url = self.bot.user.avatar
        else:
            doc = list(self.col.find({"owner_id": member.id}).sort("uses", -1))
            title = f"{member.display_name}'s Tags"
            icon_url = ctx.author.display_avatar

        if len(doc) == 0:
            raise commands.BadArgument(f"{member.display_name} does not have any tags.")

        pages = self.page_source(doc, title=title, icon_url=icon_url)
        view = plasma.Pagination(ctx, pages)
        view.message = await ctx.send(embed=pages[0], view=view)

def setup(bot):
    bot.add_cog(Tags(bot))