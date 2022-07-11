from PIL import Image
import aiohttp
from contextlib import suppress
from datetime import datetime
import hashlib
import io
import plasma

import nextcord
from nextcord.ext import commands


class Pokemon(commands.Cog):
    """For pokemon."""

    def __init__(self, bot):
        self.bot = bot
        self.col = plasma.mongo.pokemon
        self.session = aiohttp.ClientSession()

    def page_source(self, entries, *, title, icon_url, per_page=20):
        total = len(entries) // per_page
        pages = []
        front, rear = 0, 0

        for i in range(total):
            embed = nextcord.Embed(color=nextcord.Color.blue(), description="")
            front = rear
            rear += per_page

            for j in range(front, rear):
                embed.add_field(name=plasma.title(entries[j]), value=f"{plasma.Emoji.check()} Collect!")
            embed.set_author(name=title, icon_url=icon_url)
            embed.set_footer(text=f"Showing {front+1}-{rear} out of {len(entries)}.")
            pages.append(embed)

        embed = nextcord.Embed(color=nextcord.Color.blue(), description="")
        for i in range(rear, len(entries)):
            embed.add_field(name=plasma.title(entries[i]), value=f"{plasma.Emoji.check()} Collect!")
        embed.set_author(name=title, icon_url=icon_url)
        embed.set_footer(text=f"Showing {rear+1}-{len(entries)} out of {len(entries)}.")
        pages.append(embed)

        return pages

    def get_hash(self, image):
        m = hashlib.md5()
        with open(image, "rb") as f:
            while chunk := f.read(8192):
                m.update(chunk)
        return m.hexdigest()

    def make_starboard_embed(self, message):
        if message.embeds is not None:
            embed = nextcord.Embed(
                color=nextcord.Color.blue(),
                description = f"{message.embeds[0].description}\n\n**[Click to jump to message!]({message.jump_url})**" if message.embeds[0].description is not nextcord.Embed.Empty else f"**[Click to jump to message!]({message.jump_url})**",
                timestamp=datetime.utcnow()
            )
            embed.set_author(name=message.author.name, icon_url=message.author.avatar)
            embed.set_image(url=message.embeds[0].image.url)
            return embed

        embed = nextcord.Embed(
            color=nextcord.Color.blue(),
            description=message.content,
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=message.author.name, icon_url=message.author.avatar)
        return embed

    def valid_embed(self, message):
        if (
            message.embeds is None
            or message.embeds[0].title is nextcord.Embed.Empty
            or message.embeds[0].description is nextcord.Embed.Empty
            or message.embeds[0].image is nextcord.Embed.Empty
        ):
            return False
        return True

    async def send(self, ctx, message, *, image_url=None):
        embed = nextcord.Embed(
            color=nextcord.Color.green(),
            description=f"{plasma.Emoji.check()} {message}"
        )
        if image_url is not None:
            embed.set_thumbnail(url=image_url)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if (
            message.guild is None
            or message.guild.id != 994266247577485473
            or not isinstance(message.author, nextcord.Member)
            or not message.author.bot
        ):
            return

        if (
            (message.author.id == 716390085896962058 and message.content.startswith("The pokémon is")) # Poketwo
            or (message.author.id == 669228505128501258 and message.content.startswith("The wild pokémon is")) # Pokemon
            or (message.author.id == 704130818339242094 and message.content.startswith("Hint")) # Deriver
        ):
            self.bot.dispatch("hint", message)
            return

        if message.author.id == 716390085896962058 and "You" in message.content: # Poketwo
            data = message.content[message.content.find("You"):]
            channel = message.guild.get_channel(994921306963316798)

            if "caught" in data and not any(x in data for x in ("evolve", "purchase", "select")):
                if "These colors seem unusual..." in data:
                    with suppress(nextcord.HTTPException, nextcord.NotFound):
                        await message.pin()
                    embed = self.make_starboard_embed(message)
                    await channel.send(f"<#{message.channel.id}>", embed=embed)
                    return

                if any(x in data.lower() for x in plasma.RARE_POKEMONS):
                    async for msg in message.channel.history(limit=30):
                        if self.valid_embed(msg):
                            embed = self.make_starboard_embed(msg)
                            await channel.send(f"<#{message.channel.id}>", embed=embed)
                            return

        if message.author.id == 669228505128501258 and "you" in message.content: # Pokemon
            data = message.content[message.content.find("you"):]
            channel = message.guild.get_channel(994923221038157906)

            if "caught" in data and not any(x in data for x in ("evolve", "purchase", "select")):
                if "Shiny" in data:
                    with suppress(nextcord.HTTPException, nextcord.NotFound):
                        await message.pin()
                    embed = self.make_starboard_embed(message)
                    await channel.send(f"<#{message.channel.id}>", embed=embed)
                    return

        if message.author.id == 716390085896962058: # Poketwo
            if self.valid_embed(message):
                if "Guess the pokémon" in message.embeds[0].description:
                    self.bot.dispatch("spawn", message)

                if "fled" in message.embeds[0].title and any(x in message.embeds[0].title.lower() for x in plasma.RARE_POKEMONS):
                    channel = message.guild.get_channel(994921306963316798)
                    i = 0

                    async for msg in message.channel.history(limit=30):
                        if self.valid_embed(msg):
                            i += 1
                            if i == 2:
                                embed = self.make_starboard_embed(msg)
                                await channel.send(f"<#{message.channel.id}>", embed=embed)
                                return

        if message.author.id == 669228505128501258: # Pokemon
            if self.valid_embed(message):
                if "Guess the pokémon" in message.embeds[0].description:
                    self.bot.dispatch("spawn", message, "pokemon", 994923221038157906, 994960527287668826)

        if message.author.id == 705016654341472327: # Pokecord
            if self.valid_embed(message):
                if "Use" in message.embeds[0].description:
                    self.bot.dispatch("spawn", message, "pokecord", 994923747893063700, 994960678366494782)

        if message.author.id == 704130818339242094: # Deriver
            if self.valid_embed(message):
                if "Guess the pokémon" in message.embeds[0].description:
                    self.bot.dispatch("spawn", message, "deriver", 994924224089169931, 994960742103142420)

    @commands.Cog.listener()
    async def on_hint(self, message):
        choices = []
        check = None

        if message.author.id == 716390085896962058: # Poketwo
            hint = message.content.replace("\_", "_").replace("The pokémon is ", "").replace(" ", "_").lower()[:-1]
        elif message.author.id == 669228505128501258: # Pokemon
            hint = message.content.replace("\_", "_").replace("The wild pokémon is ", "").replace(" ", "_").lower()
        elif message.author.id == 704130818339242094: # Deriver
            hint = message.content.replace("\_", "_").replace("Hint: ", "").replace("`", "").replace(" ", "_").lower()

        for pokemon in plasma.POKEMONS:
            if len(pokemon) == len(hint):
                for i in range(len(pokemon)):
                    if hint[i] != "_":
                        if pokemon[i] == hint[i]:
                            check = True
                        else:
                            check = False
                            break
                
                if check:
                    choices.append(plasma.title(pokemon))

        if len(choices) > 0:
            await message.channel.send("> **" + ", ".join(choices) + "**")

    @commands.Cog.listener()
    async def on_spawn(self, message, name, channel_id, role_id):
        async with self.session.get(message.embeds[0].image.url) as f:
            Image.open(io.BytesIO(await f.read())).save(f"assets/{name}.png")

        hash = self.get_hash(f"assets/{name}.png")
        doc = self.col.find_one({"hash": hash})
        rarity = ("legendary", "mythical", "ultra beast", "event", "other") if message.author.id != 705016654341472327 else ("legendary", "mythical", "event", "other")

        if doc is None:
            doc = self.col.find_one({"hashes": hash})

        if doc is not None:
            channel = message.guild.get_channel(channel_id)

            if any(x == doc["rarity"] for x in rarity):
                role = message.guild.get_role(role_id)
                await message.channel.send(f"{role.mention} Look it could be a **{plasma.title(doc['name'])}**.")

                embed = self.make_starboard_embed(message)
                await channel.send(f"<#{message.channel.id}>", embed=embed)

            hunter = list(plasma.mongo.member.find({name: doc["name"]}))
            if len(hunter) > 0:
                hunters = " ".join(f"<@{hunter['_id']}>")
                await message.channel.send(f"**{plasma.title(doc['name'])}:** {hunters}")


    @plasma.community_and_test_server_only()
    @commands.command()
    async def add(self, ctx, bot: plasma.BotConverter, *, pokemon: plasma.SpeciesConverter):
        """Adds your tag to auto pinging list."""

        name = bot.name.replace("é", "e").lower()
        doc = plasma.mongo.find_member(ctx.author)

        if (
            len(doc[name.lower()]) > 0
            and not ctx.author.id in plasma.OWNERS
            and not any(ctx.author.id == x for x in (994927712135286828, 994927785351053362, 995608606609252406))
            and not ctx.guild.premium_subscriber_role in ctx.author.roles
        ):
            raise commands.BadArgument("You must be a server booster to add more than 1 pokemon.")

        if pokemon["name"] in doc[name]:
            raise commands.BadArgument("That pokemon already exists in your collection.")

        plasma.mongo.update_member(ctx.author, {"$push": {name: pokemon["name"]}})
        await self.send(
            ctx, f"Added {ctx.author.mention} to `{pokemon['name']}` tag.",
            image_url=f"https://raw.githubusercontent.com/Infernus07/data/master/pokemons/normal/{pokemon['_id']}.png"
        )

    @plasma.community_and_test_server_only()
    @commands.command()
    async def remove(self, ctx, bot: plasma.BotConverter, *, pokemon: plasma.SpeciesConverter):
        """Removes your tag from auto pinging list."""

        name = bot.name.replace("é", "e").lower()
        doc = plasma.mongo.find_member(ctx.author)

        if pokemon["name"] not in doc[name]:
            raise commands.BadArgument("You don't have that pokemon in your list.")

        plasma.mongo.update_member(ctx.author, {"$pull": {name: pokemon["name"]}})
        await self.send(
            ctx, f"Removed {ctx.author.mention} from `{pokemon['name']}` tag.",
            image_url=f"https://raw.githubusercontent.com/Infernus07/data/master/pokemons/normal/{pokemon['_id']}.png"
        )

    @plasma.community_and_test_server_only()
    @commands.command()
    async def clear(self, ctx, bot: plasma.BotConverter):
        """Removes all of your tags from auto pinging list."""

        name = bot.name.replace("é", "e").lower()
        doc = plasma.mongo.find_member(ctx.author)

        if len(doc[name]) == 0:
            raise commands.BadArgument(f"You don't have any tag in {bot.name} bot.")

        confirm = await plasma.get_confirmation(ctx, f"Are you sure you want to remove **all** of your tags in **{bot.name}** bot?")
        if confirm:
            plasma.mongo.update_member(ctx.author, {"$set": {name: []}})
            await self.send(ctx, f"Removed all of your tags from {bot.name} bot.", image_url=bot.avatar)

    @plasma.community_and_test_server_only()
    @commands.command()
    async def view(self, ctx, bot: plasma.BotConverter, *, pokemon: plasma.SpeciesConverter):
        """Shows lists of pokemon hunters in a bot."""

        name = bot.name.replace("é", "e").lower()
        hunter = list(plasma.mongo.member.find({name: pokemon["name"]}))
        if len(hunter) > 0:
            hunters = " ".join(f"<@{hunter['_id']}>")
        else:
            hunters = "[None]"

        embed = nextcord.Embed(
            color=nextcord.Color.blue(),
            title="Tag List: " + plasma.title(pokemon["name"]),
            description=hunters,
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=bot.name, icon_url=bot.avatar)
        embed.set_footer(text="Your ID is in this tag!" if f"<@{ctx.author.id}>" in hunters else "Your ID is not in this tag.")
        embed.set_thumbnail(url=f"https://raw.githubusercontent.com/Infernus07/data/master/pokemons/normal/{pokemon['_id']}.png")

        await ctx.send(embed=embed)

    @plasma.community_and_test_server_only()
    @commands.command()
    async def view(self, ctx, bot: plasma.BotConverter, *, member: nextcord.Member = None):
        """Shows collection list of a user."""

        member = member or ctx.author
        name = bot.name.replace("é", "e").lower()
        doc = plasma.mongo.find_member(member)

        if len(doc[name]) == 0:
            raise commands.BadArgument(f"{member.display_name} does not have any tags in `{bot.name}` bot.")

        pages = self.page_source(doc[name], title=f"{member.display_name}'s Tags", icon_url=bot.avatar)
        view = plasma.Pagination(ctx, pages)
        view.message = await ctx.send(embed=pages[0], view=view)

def setup(bot):
    bot.add_cog(Pokemon(bot))